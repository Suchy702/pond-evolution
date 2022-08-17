from __future__ import annotations

import functools
from functools import reduce
from random import random
from typing import cast, Type, Generator, Optional

from src.ai.ai import AI
from src.ai.alga_ai import AlgaAI
from src.ai.alga_maker_ai import AlgaMakerAI
from src.ai.fish_ai import FishAI
from src.ai.worm_ai import WormAI
from src.decision.decision_set import DecisionSet
from src.events.event import LogicEvent
from src.events.event_emitter import EventEmitter
from src.object.dummy_type import DummyType
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.fish_type import FishType
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.object_handler.fish_handler import FishHandler
from src.object_handler.plant_handler import PlantHandler
from src.object_handler.pond_object_handler import PondObjectHandler, PondObjectHandlerHomogeneous
from src.object_handler.worm_handler import WormHandler
from src.pond.pond_viewer import PondViewer
from src.position import Position
from src.simulation_settings import SimulationSettings

from src.constants import PREDATOR_CHANCE_TO_DEFENCE

event_emitter = EventEmitter()


class Interactor:
    def __init__(self, settings: SimulationSettings):
        self._fish_handler: FishHandler = FishHandler(settings)
        self._worm_handler: WormHandler = WormHandler(settings)
        self._plant_handler: PlantHandler = PlantHandler(settings)
        # Order of handlers and AI classes is important
        self.handlers: list[PondObjectHandler] = [self._plant_handler, self._worm_handler, self._fish_handler]
        self.ai_classes: list[Type[AI] | tuple[Type[AI], ...]] = [(AlgaAI, AlgaMakerAI), WormAI, FishAI]

        self._pond_viewer = PondViewer(settings.pond_width, settings.pond_height)
        for handler in self.handlers:
            self._pond_viewer.add_ponds(handler.ponds)

    @property
    def all_objects(self) -> list[PondObject]:
        return reduce(lambda list_, handler: list_ + handler.objects, self.handlers, [])

    def _get_decisions(self) -> Generator[tuple[DecisionSet, int], None, None]:
        for idx, (handler, ai_classes) in enumerate(zip(self.handlers, self.ai_classes)):
            if isinstance(ai_classes, tuple):
                for ai in ai_classes:
                    yield ai.get_general_decisions(), idx
            else:
                yield ai_classes.get_general_decisions(), idx
            for decisions in handler.get_decisions(self._pond_viewer):
                yield decisions, idx

    def handle_decisions(self) -> None:
        for decisions, handler_idx in self._get_decisions():
            self.handlers[handler_idx].handle_decisions(decisions)
            self._handle_decisions(decisions)

    def _handle_decisions(self, decisions: DecisionSet) -> None:
        pass

    def prepare(self) -> None:
        self._plant_handler.alga_maker_handler.add_random(10)
        self._fish_handler.add_random(50)

    def _is_food_at_pos(self, pos: Position) -> bool:
        return self._worm_handler.is_sth_at_pos(pos) or self._plant_handler.alga_handler.is_sth_at_pos(pos)

    def _is_predator_eating(self, fish: Fish) -> bool:
        return FishTrait.PREDATOR in fish.traits and len(self._fish_handler.get_spot_obj(fish.pos)) > 1

    def _find_pos_where_eat(self) -> list[Position]:
        pos_where_eat = []
        for fish in self._fish_handler.fishes:
            if self._is_food_at_pos(fish.pos) or self._is_predator_eating(fish):
                pos_where_eat.append(fish.pos)
        return pos_where_eat

    def _eat_at_spot(self, pos: Position) -> None:
        self.eat_other_non_fish_at_spot(pos)
        self.eat_other_fish_at_spot(pos)

    def _cnt_fish_eating_specific_food(self, pos: Position, fish_types: list[FishType]) -> int:
        cnt_fishes = 0
        for fish in self._fish_handler.get_spot_obj(pos):
            fish = cast(Fish, fish)
            if FishTrait.PREDATOR in fish.traits:
                continue
            if fish.fish_type in fish_types:
                cnt_fishes += 1
        return cnt_fishes

    def _change_energy_fish_which_ate(self, pos: Position, worm_eating_val: int, algae_eating_val: int) -> None:
        for fish in self._fish_handler.get_spot_obj(pos):
            fish = cast(Fish, fish)
            if FishTrait.PREDATOR in fish.traits:
                continue
            if fish.fish_type in [FishType.OMNIVORE, FishType.CARNIVORE]:
                fish.vitality += worm_eating_val
            if fish.fish_type in [FishType.OMNIVORE, FishType.HERBIVORE]:
                fish.vitality += algae_eating_val

    def _calc_worm_eating_val(self, pos: Position) -> int:
        worm_energy_val = self._worm_handler.get_spot_energy_val(pos)
        cnt_fish_eating_worms = self._cnt_fish_eating_specific_food(pos, [FishType.OMNIVORE, FishType.CARNIVORE])
        return 0 if cnt_fish_eating_worms == 0 else worm_energy_val // cnt_fish_eating_worms

    def _calc_algae_eating_val(self, pos: Position) -> int:
        algae_energy_val = self._plant_handler.alga_handler.get_spot_energy_val(pos)
        cnt_fish_eating_algae = self._cnt_fish_eating_specific_food(pos, [FishType.OMNIVORE, FishType.HERBIVORE])
        return 0 if cnt_fish_eating_algae == 0 else algae_energy_val // cnt_fish_eating_algae

    def _remove_ate_objects(self, pos: Position) -> None:
        self._worm_handler.remove_at_spot(pos)
        self._plant_handler.alga_handler.remove_at_spot(pos)

    def eat_other_non_fish_at_spot(self, pos: Position) -> None:
        self._change_energy_fish_which_ate(pos, self._calc_worm_eating_val(pos), self._calc_algae_eating_val(pos))
        self._remove_ate_objects(pos)

    def _get_fishes_at_same_spot_in_order(self, pos: Position) -> list[Fish]:
        fish = list(self._fish_handler.get_spot_obj(pos))
        fish = cast(list[Fish], fish)
        fish.sort(key=functools.cmp_to_key(lambda a, b: a.size - b.size))  # type: ignore
        return fish

    def _can_fish_eat_other_fish(self, eaten_fish: Fish, other_fish: Fish) -> bool:
        return FishTrait.PREDATOR in other_fish.traits and eaten_fish.size < other_fish.size

    def _cnt_bigger_predators(self, i: int, fishes: list[Fish]) -> int:
        cnt_bigger_predators = 0
        for j in range(i + 1, len(fishes)):
            if self._can_fish_eat_other_fish(fishes[i], fishes[j]):
                cnt_bigger_predators += 1
        return cnt_bigger_predators

    def _feed_predators(self, i: int, cnt_bigger_predators: int, fishes: list[Fish]) -> None:
        for j in range(i + 1, len(fishes)):
            if self._can_fish_eat_other_fish(fishes[i], fishes[j]):
                fishes[j].vitality += fishes[i].vitality // cnt_bigger_predators

    def _can_predator_defend_himself(self, fish: Fish) -> bool:
        return FishTrait.PREDATOR in fish.traits and random() < PREDATOR_CHANCE_TO_DEFENCE

    def eat_other_fish_at_spot(self, pos: Position) -> None:
        fishes = self._get_fishes_at_same_spot_in_order(pos)

        for i in range(len(fishes)):
            if self._can_predator_defend_himself(fishes[i]):
                continue

            cnt_bigger_predators = self._cnt_bigger_predators(i, fishes)
            if cnt_bigger_predators == 0:
                continue

            fishes[i].is_eaten = True
            self._feed_predators(i, cnt_bigger_predators, fishes)

    def feed_fish(self) -> None:
        for pos in self._find_pos_where_eat():
            self._eat_at_spot(pos)

    def remove_unnecessary_objects(self) -> None:
        self._fish_handler.remove_dead_fish()
        self._worm_handler.remove_worms_on_the_ground()
        self._plant_handler.alga_handler.remove_algae_on_surface()

    def _dispatch_handler(self, kind: ObjectKind) -> PondObjectHandlerHomogeneous:
        match kind:
            case ObjectKind.WORM:
                return self._worm_handler
            case ObjectKind.ALGA:
                return self._plant_handler.alga_handler
            case ObjectKind.ALGA_MAKER:
                return self._plant_handler.alga_maker_handler
            case ObjectKind.FISH:
                return self._fish_handler

    def add_obj_by_click(self, event: LogicEvent) -> None:
        event.obj.pos = event.pos
        handler = self._dispatch_handler(event.obj.kind)
        handler.add(event.obj)

    def _get_non_fish_dummy(self, dummy_type: DummyType) -> Optional[PondObject]:
        match dummy_type:
            case DummyType.ALGA:
                return self._plant_handler.alga_handler.create_random_single()
            case DummyType.ALGA_MAKER:
                return self._plant_handler.alga_maker_handler.create_random_single()
            case DummyType.WORM:
                return self._worm_handler.create_random_single()
            case _:
                return None

    def _create_basic_dummy_fish(self) -> Fish:
        fish = self._fish_handler.create_random_single()
        fish = cast(Fish, fish)
        fish.traits.clear()
        fish.traits.add(FishTrait.SMART)
        return fish

    def _get_fish_dummy(self, dummy_type: DummyType) -> Fish:
        fish = self._create_basic_dummy_fish()
        match dummy_type:
            case DummyType.FISH_HERBIVORE:
                fish.fish_type = FishType.HERBIVORE
            case DummyType.FISH_CARNIVORE:
                fish.fish_type = FishType.CARNIVORE
            case DummyType.FISH_OMNIVORE:
                fish.fish_type = FishType.OMNIVORE
            case DummyType.FISH_PREDATOR:
                fish.fish_type = FishType.CARNIVORE
                fish.traits.add(FishTrait.PREDATOR)
        return fish

    def get_dummy(self, dummy_type: DummyType) -> PondObject:
        dummy = self._get_non_fish_dummy(dummy_type)
        if dummy is not None:
            return dummy
        return self._get_fish_dummy(dummy_type)

    def objects_by_type(self, obj_type: ObjectKind) -> list[PondObject]:
        return self._dispatch_handler(obj_type).objects

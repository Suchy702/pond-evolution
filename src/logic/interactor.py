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

    def setup(self) -> None:
        self._plant_handler.alga_maker_handler.add_random(10)
        self._fish_handler.add_random(50)

    def handle_decisions(self) -> None:
        for decisions, handler_idx in self._get_decisions():
            self.handlers[handler_idx].handle_decisions(decisions)
            self._handle_decisions(decisions)

    def feed_fish(self) -> None:
        for position in self._find_eating_spots():
            self._eat_at_spot(position)

    def remove_unnecessary_objects(self) -> None:
        self._fish_handler.remove_dead_fish()
        self._worm_handler.remove_worms_on_ground()
        self._plant_handler.alga_handler.remove_algae_on_surface()

    def add_object_by_click(self, event: LogicEvent) -> None:
        event.pond_object.position = event.position
        handler = self._dispatch_handler(event.pond_object.kind)
        handler.add(event.pond_object)

    def get_dummy(self, dummy_type: DummyType) -> PondObject:
        dummy = self._get_non_fish_dummy(dummy_type)
        if dummy is not None:
            return dummy
        return self._get_fish_dummy(dummy_type)

    def get_objects_by_type(self, object_type: ObjectKind) -> list[PondObject]:
        return self._dispatch_handler(object_type).objects

    def _get_decisions(self) -> Generator[tuple[DecisionSet, int], None, None]:
        for idx, (handler, ai_classes) in enumerate(zip(self.handlers, self.ai_classes)):
            if isinstance(ai_classes, tuple):
                for ai in ai_classes:
                    yield ai.get_general_decisions(), idx
            else:
                yield ai_classes.get_general_decisions(), idx
            for decisions in handler.get_decisions(self._pond_viewer):
                yield decisions, idx

    def _handle_decisions(self, decisions: DecisionSet) -> None:
        pass

    def _find_eating_spots(self) -> list[Position]:
        eating_spots = []
        for fish in self._fish_handler.fishes:
            if self._is_food_at_position(fish.position) or self._is_predator_eating(fish):
                eating_spots.append(fish.position)
        return eating_spots

    def _is_food_at_position(self, position: Position) -> bool:
        return self._worm_handler.is_position_nonempty(position) or self._plant_handler.alga_handler.is_position_nonempty(position)

    def _is_predator_eating(self, fish: Fish) -> bool:
        return FishTrait.PREDATOR in fish.traits and len(self._fish_handler.get_spot_objects(fish.position)) > 1

    def _eat_at_spot(self, position: Position) -> None:
        self._eat_other_non_fish_at_spot(position)
        self._eat_other_fish_at_spot(position)

    def _eat_other_non_fish_at_spot(self, position: Position) -> None:
        self._update_fish_vitality(
            position, self._get_worm_energy_distribution(position), self._get_alga_energy_distribution(position)
        )
        self._remove_eaten_objects(position)

    def _eat_other_fish_at_spot(self, position: Position) -> None:
        fishes = self._get_fish_at_spot_in_order(position)

        for i in range(len(fishes)):
            if self._can_predator_defend_himself(fishes[i]):
                continue

            count_bigger_predators = self._count_bigger_predators(i, fishes)
            if count_bigger_predators == 0:
                continue

            fishes[i].is_eaten = True
            self._feed_predators(i, count_bigger_predators, fishes)

    def _count_fish_eating_specific_food(self, position: Position, fish_types: list[FishType]) -> int:
        count_fishes = 0
        for fish in self._fish_handler.get_spot_objects(position):
            fish = cast(Fish, fish)
            if FishTrait.PREDATOR in fish.traits:
                continue
            if fish.fish_type in fish_types:
                count_fishes += 1
        return count_fishes

    def _get_alga_energy_distribution(self, position: Position) -> int:
        algae_energy_value = self._plant_handler.alga_handler.get_spot_energy_value(position)
        count_fish_eating_algae = self._count_fish_eating_specific_food(
            position, [FishType.OMNIVORE, FishType.HERBIVORE]
        )
        return 0 if count_fish_eating_algae == 0 else algae_energy_value // count_fish_eating_algae

    def _get_worm_energy_distribution(self, position: Position) -> int:
        worm_energy_value = self._worm_handler.get_spot_energy_value(position)
        count_fish_eating_worms = self._count_fish_eating_specific_food(
            position, [FishType.OMNIVORE, FishType.CARNIVORE]
        )
        return 0 if count_fish_eating_worms == 0 else worm_energy_value // count_fish_eating_worms

    def _update_fish_vitality(self, position: Position, worm_eating_value: int, alga_eating_value: int) -> None:
        for fish in self._fish_handler.get_spot_objects(position):
            fish = cast(Fish, fish)
            if FishTrait.PREDATOR in fish.traits:
                continue
            if fish.fish_type in [FishType.OMNIVORE, FishType.CARNIVORE]:
                fish.vitality += worm_eating_value
            if fish.fish_type in [FishType.OMNIVORE, FishType.HERBIVORE]:
                fish.vitality += alga_eating_value

    def _remove_eaten_objects(self, position: Position) -> None:
        self._worm_handler.remove_at_spot(position)
        self._plant_handler.alga_handler.remove_at_spot(position)

    def _get_fish_at_spot_in_order(self, position: Position) -> list[Fish]:
        fish = list(self._fish_handler.get_spot_objects(position))
        fish = cast(list[Fish], fish)
        fish.sort(key=functools.cmp_to_key(lambda a, b: a.size - b.size))  # type: ignore
        return fish

    def _feed_predators(self, i: int, count_bigger_predators: int, fishes: list[Fish]) -> None:
        for j in range(i + 1, len(fishes)):
            if self._can_fish_eat_other_fish(fishes[i], fishes[j]):
                fishes[j].vitality += fishes[i].vitality // count_bigger_predators

    @staticmethod
    def _can_fish_eat_other_fish(eaten_fish: Fish, other_fish: Fish) -> bool:
        return FishTrait.PREDATOR in other_fish.traits and eaten_fish.size < other_fish.size

    def _count_bigger_predators(self, i: int, fishes: list[Fish]) -> int:
        cnt_bigger_predators = 0
        for j in range(i + 1, len(fishes)):
            if self._can_fish_eat_other_fish(fishes[i], fishes[j]):
                cnt_bigger_predators += 1
        return cnt_bigger_predators

    @staticmethod
    def _can_predator_defend_himself(fish: Fish) -> bool:
        return FishTrait.PREDATOR in fish.traits and random() < PREDATOR_CHANCE_TO_DEFENCE

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
            case _:
                return None

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

    def _create_basic_dummy_fish(self) -> Fish:
        fish = self._fish_handler.create_random_single()
        fish = cast(Fish, fish)
        fish.traits.clear()
        fish.traits.add(FishTrait.SMART)
        return fish

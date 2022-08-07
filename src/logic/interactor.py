from __future__ import annotations

import functools
from functools import reduce
from random import random
from typing import cast, Type, Generator

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

    # beta function for testing
    def preparations(self) -> None:
        self._plant_handler.add_random(10)
        self._fish_handler.add_random(50)

    def _find_pos_where_eat(self) -> list[Position]:
        pos_where_eat = []
        for fish in self._fish_handler.fishes:
            if self._worm_handler.is_sth_at_pos(fish.pos) or \
                    self._plant_handler.alga_handler.is_sth_at_pos(fish.pos) or \
                    (FishTrait.PREDATOR in fish.traits and len(self._fish_handler.get_spot_obj(fish.pos)) > 1):
                pos_where_eat.append(fish.pos)
        return pos_where_eat

    def _eat_at_spot(self, pos: Position) -> None:
        self.eat_other_non_fish_at_spot(pos)
        self.eat_other_fish_at_spot(pos)

    def eat_other_non_fish_at_spot(self, pos: Position) -> None:
        worm_energy_val = self._worm_handler.get_spot_energy_val(pos)
        algae_energy_val = self._plant_handler.alga_handler.get_spot_energy_val(pos)

        cnt_fish_that_will_eat_worm = 0
        cnt_fish_that_will_eat_algae = 0
        for fish in self._fish_handler.get_spot_obj(pos):
            fish = cast(Fish, fish)
            if FishTrait.PREDATOR in fish.traits:
                continue
            if fish.fish_type in [FishType.OMNIVORE, FishType.CARNIVORE]:
                cnt_fish_that_will_eat_worm += 1
            if fish.fish_type in [FishType.OMNIVORE, FishType.HERBIVORE]:
                cnt_fish_that_will_eat_algae += 1

        for fish in self._fish_handler.get_spot_obj(pos):
            fish = cast(Fish, fish)
            if FishTrait.PREDATOR in fish.traits:
                continue
            if fish.fish_type in [FishType.OMNIVORE, FishType.CARNIVORE]:
                fish.vitality += worm_energy_val // cnt_fish_that_will_eat_worm
            if fish.fish_type in [FishType.OMNIVORE, FishType.HERBIVORE]:
                fish.vitality += algae_energy_val // cnt_fish_that_will_eat_algae

        self._worm_handler.remove_at_spot(pos)
        self._plant_handler.alga_handler.remove_at_spot(pos)

    def eat_other_fish_at_spot(self, pos: Position) -> None:
        fish = list(self._fish_handler.get_spot_obj(pos))
        fish = cast(list[Fish], fish)
        fish.sort(key=functools.cmp_to_key(lambda a, b: a.size - b.size))  # type: ignore

        for i in range(len(fish)):
            if FishTrait.PREDATOR in fish[i].traits and random() < 0.5:
                continue

            cnt_bigger_predators = 0
            for j in range(i + 1, len(fish)):
                if FishTrait.PREDATOR in fish[j].traits and fish[i].size < fish[j].size:
                    cnt_bigger_predators += 1

            if cnt_bigger_predators == 0:
                continue

            fish[i].is_eaten = True
            for j in range(i + 1, len(fish)):
                if FishTrait.PREDATOR in fish[j].traits and fish[i].size < fish[j].size:
                    fish[j].vitality += fish[i].vitality // cnt_bigger_predators

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
        return None

    def add_obj_by_click(self, event: LogicEvent) -> None:
        event.obj.pos = event.pos
        handler = self._dispatch_handler(event.obj.kind)
        handler.add(event.obj)

    def get_dummy(self, dummy_type: DummyType) -> PondObject:
        match dummy_type:
            case DummyType.ALGA:
                return self._plant_handler.alga_handler.create_random_single()
            case DummyType.ALGA_MAKER:
                return self._plant_handler.alga_maker_handler.create_random_single()
            case DummyType.WORM:
                return self._worm_handler.create_random_single()

        fish = self._fish_handler.create_random_single()
        fish = cast(Fish, fish)
        fish.traits.clear()
        fish.traits.add(FishTrait.SMART)

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

    def objects_by_type(self, obj_type: ObjectKind) -> list[PondObject]:
        return self._dispatch_handler(obj_type).objects

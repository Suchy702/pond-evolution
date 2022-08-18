import functools
import itertools
from random import randint, random
from typing import cast, Generator

from overrides import overrides

from src.constants import (
    FISH_MIN_EYESIGHT,
    FISH_MAX_EYESIGHT,
    FISH_MIN_SPEED,
    FISH_MAX_SPEED,
    FISH_MIN_SIZE,
    FISH_MAX_SIZE,
    CHANCE_TO_BE_SMART,
    CHANCE_TO_BE_PREDATOR,
)
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.fish_type import FishType
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.pond.pond_viewer import PondViewer
from src.position import Position
from src.simulation_settings import SimulationSettings


class FishHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def fishes(self) -> list[Fish]:
        objects = cast(list[Fish], self.objects)
        return objects

    @overrides
    def create_random_single(self) -> PondObject:
        fish = self._create_basic_random_fish()
        fish.fish_type = FishType.get_random()
        self._add_advanced_traits(fish)
        return fish

    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> Generator[DecisionSet, None, None]:
        sorted_fish = sorted(self.fishes, key=functools.cmp_to_key(self._compare_by_movement_order))

        for key, group in itertools.groupby(sorted_fish, lambda f: FishTrait.PREDATOR in f.traits):
            decisions = DecisionSet()
            for fish in group:
                decisions += fish.get_decisions(pond_viewer)
            yield decisions

    def handle_decisions(self, decisions: DecisionSet):
        for decision in decisions[DecisionType.MOVE, ObjectKind.FISH]:
            self.move_fish(decision)
        for decision in decisions[DecisionType.STAY, ObjectKind.FISH]:
            self.event_emitter.emit_anim_stay_event(decision)
        for decision in decisions[DecisionType.REPRODUCE, ObjectKind.FISH]:
            fish = cast(Fish, decision.pond_object)
            self.reproduce(fish)

    def move_fish(self, decision: Decision) -> None:
        fish = cast(Fish, decision.pond_object)
        new_position = self._trim_without_ground_level(decision.to_x, decision.to_y)
        self.event_emitter.emit_anim_move_event(decision, new_position)
        fish.spoil_vitality(self.settings.size_penalty, self.settings.speed_penalty)
        self._pond.change_position(fish, new_position)

    def reproduce(self, fish: Fish) -> None:
        self.add_all(fish.reproduce())
        self.remove(fish)

    def remove_dead_fish(self) -> None:
        self.remove_all([fish for fish in self.fishes if not fish.is_alive()])

    def _create_basic_random_fish(self) -> Fish:
        speed = randint(FISH_MIN_SPEED, FISH_MAX_SPEED)
        size = randint(FISH_MIN_SIZE, FISH_MAX_SIZE)
        eyesight = randint(FISH_MIN_EYESIGHT, FISH_MAX_EYESIGHT)
        return Fish(speed, size, eyesight, self._pond.random_position())

    @staticmethod
    def _compare_by_movement_order(a: Fish, b: Fish):
        # Predators move last.
        return (FishTrait.PREDATOR in a.traits) - (FishTrait.PREDATOR in b.traits)

    def _trim_without_ground_level(self, x, y):
        new_position = self._pond.trim_position(Position(y, x))
        new_position.y = min(new_position.y, self._pond.height-2)
        return new_position

    @staticmethod
    def _is_getting_smart_trait() -> bool:
        return random() < CHANCE_TO_BE_SMART

    @staticmethod
    def _is_getting_predator_trait() -> bool:
        return random() < CHANCE_TO_BE_PREDATOR

    def _add_advanced_traits(self, fish) -> None:
        if self._is_getting_smart_trait():
            fish.traits.add(FishTrait.SMART)

        if self._is_getting_predator_trait():
            fish.add_predator_trait()

from __future__ import annotations

from random import randint, random

from src.ai.fish_ai import FishAI
from src.constants import (
    FISH_VITALITY_SPOIL_RATE,
    EVOLUTION_DEVIATION_DIV,
    MIN_FISH_TO_BIRTH,
    MAX_FISH_TO_BIRTH,
    FISH_NEED_MULTI_VITALITY_TO_BREED,
    CHANCE_TO_GET_PARENT_TRAIT,
    CHANCE_TO_GET_NEW_TRAIT,
)
from src.object.fish_trait import FishTrait
from src.object.fish_type import FishType
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.position import Position


class Fish(PondObject):
    def __init__(self, speed: int, size: int, eyesight: int, pos: Position):
        super().__init__(ObjectKind.FISH, pos, FishAI(self))
        self.fish_type: FishType = FishType.OMNIVORE
        self.traits: set[FishTrait] = set()
        self.speed: int = speed
        self.size: int = size
        self.eyesight: int = eyesight
        self.vitality: int = self.speed + self.size
        self.vitality_need_to_breed: int = self.vitality * FISH_NEED_MULTI_VITALITY_TO_BREED
        self.is_eaten: bool = False

    def spoil_vitality(self) -> None:
        self.vitality -= FISH_VITALITY_SPOIL_RATE

    def is_alive(self) -> bool:
        return self.vitality > 0 and not self.is_eaten

    def is_position_reachable(self, pos: Position) -> bool:
        return abs(self.pos.x - pos.x) <= self.speed and abs(self.pos.y - pos.y) <= self.speed

    @staticmethod
    def _calc_deviation(val: int) -> int:
        return val // EVOLUTION_DEVIATION_DIV

    def _calc_child_trait(self, min_val: int, parent_trait: int) -> int:
        parent_trait_dev = self._calc_deviation(parent_trait)
        return max(min_val, parent_trait + randint(-parent_trait_dev, parent_trait_dev))

    def _make_child(self) -> Fish:
        child_speed = self._calc_child_trait(1, self.speed)
        child_size = self._calc_child_trait(1, self.size)
        child_eyesight = self._calc_child_trait(1, self.eyesight)

        fish = Fish(child_speed, child_size, child_eyesight, self.pos)
        fish.fish_type = self.fish_type

        return fish

    @staticmethod
    def _is_getting_parent_trait() -> bool:
        return random() < CHANCE_TO_GET_PARENT_TRAIT

    @staticmethod
    def _is_getting_new_trait() -> bool:
        return random() < CHANCE_TO_GET_NEW_TRAIT

    def _add_traits_to_child(self, fish: Fish) -> None:
        for trait in self.traits:
            if self._is_getting_parent_trait():
                fish.traits.add(trait)

        if self._is_getting_new_trait():
            fish.traits.add(FishTrait.get_random())

    def _birth_fish(self) -> Fish:
        fish = self._make_child()
        self._add_traits_to_child(fish)

        if FishTrait.PREDATOR in fish.traits:
            fish.fish_type = FishType.CARNIVORE

        return fish

    def birth_fish(self) -> list[Fish]:
        return [self._birth_fish() for _ in range(randint(MIN_FISH_TO_BIRTH, MAX_FISH_TO_BIRTH))]

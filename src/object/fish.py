from __future__ import annotations

from random import randint, random

from src.ai.fish_ai import FishAI
from src.constants import (
    FISH_MIN_SPEED,
    FISH_MAX_SPEED,
    FISH_MIN_SIZE,
    FISH_MAX_SIZE,
    FISH_MIN_EYESIGHT,
    FISH_MAX_EYESIGHT,
    FISH_VITALITY_SPOIL_RATE,
    EVOLUTION_DEVIATION_DIV,
    MIN_FISH_TO_BIRTH,
    MAX_FISH_TO_BIRTH,
    FISH_NEED_MULTI_VITALITY_TO_BREED,
    CHANCE_TO_GET_PARENT_TRAIT,
    CHANCE_TO_GET_NEW_TRAIT,
)
from src.math import clip
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

        self._speed: int = None
        self._size: int = None
        self._eyesight: int = None
        self.speed = speed
        self.size = size
        self.eyesight = eyesight

        self.vitality: int = self.speed + self.size
        self.vitality_need_to_breed: int = self.vitality * FISH_NEED_MULTI_VITALITY_TO_BREED
        self.is_eaten: bool = False

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, val: int):
        self._speed = clip(val, FISH_MIN_SPEED, FISH_MAX_SPEED)

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, val: int):
        self._size = clip(val, FISH_MIN_SIZE, FISH_MAX_SIZE)

    @property
    def eyesight(self) -> int:
        return self._eyesight

    @eyesight.setter
    def eyesight(self, val: int):
        self._eyesight = clip(val, FISH_MIN_EYESIGHT, FISH_MAX_EYESIGHT)

    def spoil_vitality(self) -> None:
        self.vitality -= FISH_VITALITY_SPOIL_RATE

    def is_alive(self) -> bool:
        return self.vitality > 0 and not self.is_eaten

    def is_position_reachable(self, pos: Position) -> bool:
        return abs(self.pos.x - pos.x) <= self.speed and abs(self.pos.y - pos.y) <= self.speed

    @staticmethod
    def _calc_deviation(val: int) -> int:
        return val // EVOLUTION_DEVIATION_DIV

    def _calc_child_trait(self, parent_trait: int) -> int:
        parent_trait_dev = self._calc_deviation(parent_trait)
        return parent_trait + randint(-parent_trait_dev, parent_trait_dev)

    def _make_child(self) -> Fish:
        child_speed = self._calc_child_trait(self.speed)
        child_size = self._calc_child_trait(self.size)
        child_eyesight = self._calc_child_trait(self.eyesight)

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
            if (trait := FishTrait.get_random()) == FishTrait.PREDATOR:
                self.add_predator_trait()
            else:
                fish.traits.add(trait)

    def add_predator_trait(self) -> None:
        self.traits.add(FishTrait.PREDATOR)
        self.fish_type = FishType.CARNIVORE
        self.eyesight -= 5
        self.speed += 5
        self.size += 5

    def _birth_fish(self) -> Fish:
        fish = self._make_child()
        self._add_traits_to_child(fish)

        if FishTrait.PREDATOR in fish.traits:
            fish.fish_type = FishType.CARNIVORE

        return fish

    def birth_fish(self) -> list[Fish]:
        return [self._birth_fish() for _ in range(randint(MIN_FISH_TO_BIRTH, MAX_FISH_TO_BIRTH))]

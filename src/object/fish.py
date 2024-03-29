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
    FISH_VITALITY_SPOIL_COEFF,
    EVOLUTION_DEVIATION_DIV,
    MIN_FISH_REPRODUCE_AMOUNT,
    MAX_FISH_REPRODUCE_AMOUNT,
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
    def __init__(self, speed: int, size: int, eyesight: int, position: Position):
        super().__init__(ObjectKind.FISH, position, FishAI(self))
        self.fish_type: FishType = FishType.OMNIVORE
        self.traits: set[FishTrait] = set()

        self._speed: int = None
        self._size: int = None
        self._eyesight: int = None
        self.speed = speed
        self.size = size
        self.eyesight = eyesight

        self.vitality: int = self.speed + self.size
        self.reproduction_vitality: int = self.vitality * FISH_NEED_MULTI_VITALITY_TO_BREED
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

    def spoil_vitality(self, size_penalty: int, speed_penalty: int) -> None:
        size_percentage = (self.size - FISH_MIN_SIZE) / (FISH_MAX_SIZE - FISH_MIN_SIZE)
        speed_percentage = (self.speed - FISH_MIN_SPEED) / (FISH_MAX_SPEED - FISH_MIN_SPEED)
        self.vitality -= int(
            FISH_VITALITY_SPOIL_COEFF * (size_penalty / 100 * size_percentage + speed_penalty / 100 * speed_percentage)
        )

    def add_predator_trait(self) -> None:
        self.traits.add(FishTrait.PREDATOR)
        self.fish_type = FishType.CARNIVORE
        self.eyesight -= 5
        self.speed += 5
        self.size += 5

    def reproduce(self) -> list[Fish]:
        return [self._reproduce() for _ in range(randint(MIN_FISH_REPRODUCE_AMOUNT, MAX_FISH_REPRODUCE_AMOUNT))]

    def is_alive(self) -> bool:
        return self.vitality > 0 and not self.is_eaten

    def is_position_reachable(self, position: Position) -> bool:
        return abs(self.position.x - position.x) <= self.speed and abs(self.position.y - position.y) <= self.speed

    def _reproduce(self) -> Fish:
        fish = self._make_child()
        self._add_traits_to_child(fish)

        if FishTrait.PREDATOR in fish.traits:
            fish.fish_type = FishType.CARNIVORE

        return fish

    def _make_child(self) -> Fish:
        child_speed = self._get_child_trait(self.speed)
        child_size = self._get_child_trait(self.size)
        child_eyesight = self._get_child_trait(self.eyesight)

        fish = Fish(child_speed, child_size, child_eyesight, self.position)
        fish.fish_type = self.fish_type

        return fish

    def _get_child_trait(self, parent_trait: int) -> int:
        parent_trait_dev = self._get_deviation(parent_trait)
        return parent_trait + randint(-parent_trait_dev, parent_trait_dev)

    @staticmethod
    def _get_deviation(val: int) -> int:
        return val // EVOLUTION_DEVIATION_DIV

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

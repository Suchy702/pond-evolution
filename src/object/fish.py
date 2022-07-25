from __future__ import annotations

from random import randint, random

from src.ai.fish_ai import FishAI
from src.constants import FISH_VITALITY_SPOIL_RATE, EVOLUTION_DEVIATION_DIV, MIN_FISH_TO_BIRTH, MAX_FISH_TO_BIRTH, \
    FISH_NEED_MULTI_VITALITY_TO_BREED
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

    def is_position_reachable(self, pos: Position):
        return abs(self.pos.x - pos.x) <= self.speed and abs(self.pos.y - pos.y) <= self.speed

    @staticmethod
    def _calc_deviation(val):
        return val // EVOLUTION_DEVIATION_DIV

    def _birth_fish(self) -> Fish:
        speed_dev = self._calc_deviation(self.speed)
        child_speed = max(1, self.speed + randint(-speed_dev, speed_dev))
        size_dev = self._calc_deviation(self.size)
        child_size = max(1, self.size + randint(-size_dev, size_dev))
        eyesight_dev = self._calc_deviation(self.eyesight)
        child_eyesight = max(1, self.eyesight + randint(-eyesight_dev, eyesight_dev))
        fish = Fish(child_speed, child_size, child_eyesight, self.pos)
        fish.fish_type = self.fish_type

        for trait in self.traits:
            if random() < 0.9:
                fish.traits.add(trait)

        if random() < 0.2:
            fish.traits.add(FishTrait.get_random())

        if FishTrait.PREDATOR in fish.traits and fish.fish_type == FishType.HERBIVORE:
            if random() < 0.5:
                fish.fish_type = FishType.CARNIVORE
            else:
                fish.fish_type = FishType.OMNIVORE

        return fish

    def birth_fish(self) -> list[Fish]:
        return [self._birth_fish() for _ in range(randint(MIN_FISH_TO_BIRTH, MAX_FISH_TO_BIRTH))]

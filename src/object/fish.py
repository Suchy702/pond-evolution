from __future__ import annotations

from random import randint

from src.ai.fish_ai import FishAI
from src.constants import FISH_VITALITY_SPOIL_RATE, EVOLUTION_DEVIATION_DIV, MIN_FISH_TO_BIRTH, MAX_FISH_TO_BIRTH, \
    FISH_NEED_MULTI_VITALITY_TO_BREED
from src.object.fish_trait import FishTrait
from src.object.fish_type import FishType
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class Fish(PondObject):
    def __init__(self, speed: int, size: int, pos: Position):
        super().__init__(ObjectKind.FISH, pos, FishAI(self))
        self.fish_type: FishType = FishType.OMNIVORE
        self.traits: set[FishTrait] = set()
        self.speed: int = speed
        self.size: int = size
        self.vitality: int = self.speed + self.size
        self.vitality_need_to_breed: int = self.vitality * FISH_NEED_MULTI_VITALITY_TO_BREED
        self.is_eaten: bool = False

    def spoil_vitality(self) -> None:
        self.vitality -= FISH_VITALITY_SPOIL_RATE

    def is_alive(self) -> bool:
        return self.vitality > 0 and not self.is_eaten

    @staticmethod
    def _calc_deviation(val):
        return val // EVOLUTION_DEVIATION_DIV

    def _birth_fish(self) -> Fish:
        speed_dev = self._calc_deviation(self.speed)
        child_speed = self.speed + randint(-speed_dev, speed_dev)
        size_dev = self._calc_deviation(self.size)
        child_size = self.size + randint(-size_dev, size_dev)
        return Fish(child_speed, child_size, self.pos)

    def birth_fish(self) -> list[Fish]:
        return [self._birth_fish() for _ in range(randint(MIN_FISH_TO_BIRTH, MAX_FISH_TO_BIRTH))]

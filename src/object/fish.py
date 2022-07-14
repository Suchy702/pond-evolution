from __future__ import annotations

from random import randint

import src.constants as const
from src.ai.ai import FishAI
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class Fish(PondObject):
    def __init__(self, speed: int, size: int, pos: Position):
        super().__init__(ObjectKind.FISH, pos, FishAI(self))
        self.speed: int = speed
        self.size: int = size
        self.vitality: int = self.speed + self.size
        self.vitality_need_to_breed: int = self.vitality * const.FISH_NEED_MULTI_VITALITY_TO_BREED

    def spoil_vitality(self) -> None:
        self.vitality -= const.FISH_VITALITY_SPOIL_RATE

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(randint(-self.speed, self.speed), randint(-self.speed, self.speed))

    def is_dead(self) -> bool:
        return self.vitality <= 0

    def is_breeding(self) -> bool:
        return self.vitality >= self.vitality_need_to_breed

    @staticmethod
    def _calc_deviation(val):
        return val // const.EVOLUTION_DEVIATION_DIV

    def _birth_fish(self) -> Fish:
        speed_dev = self._calc_deviation(self.speed)
        child_speed = self.speed + randint(-speed_dev, speed_dev)
        size_dev = self._calc_deviation(self.size)
        child_size = self.size + randint(-size_dev, size_dev)
        return Fish(child_speed, child_size, self.pos)

    def birth_fish(self) -> list[Fish]:
        return [self._birth_fish() for _ in range(randint(const.MIN_FISH_TO_BIRTH, const.MAX_FISH_TO_BIRTH))]

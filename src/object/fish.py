from __future__ import annotations

from random import randint

import src.constants as const
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class Fish(PondObject):
    def __init__(self, speed: int, size: int, pos: Position):
        super().__init__(ObjectKind.FISH, pos)
        self._speed: int = speed
        self._size: int = size
        self._vitality: int = self._speed + self._size
        self._vitality_need_to_breed: int = self._vitality * const.FISH_NEED_MULTI_VITALITY_TO_BREED

    @property
    def vitality(self) -> int:
        return self._vitality

    @vitality.setter
    def vitality(self, val):
        self._vitality = val

    def spoil_vitality(self) -> None:
        self._vitality -= const.FISH_VITALITY_SPOIL_RATE

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(randint(-self._speed, self._speed), randint(-self._speed, self._speed))

    def is_dead(self) -> bool:
        return self.vitality <= 0

    def is_breeding(self) -> bool:
        return self._vitality >= self._vitality_need_to_breed

    @staticmethod
    def _calc_deviation(val):
        return val // const.EVOLUTION_DEVIATION_DIV

    def _birth_fish(self) -> Fish:
        speed_dev = self._calc_deviation(self._speed)
        child_speed = self._speed + randint(-speed_dev, speed_dev)
        size_dev = self._calc_deviation(self._size)
        child_size = self._size + randint(-size_dev, size_dev)
        return Fish(child_speed, child_size, self.pos)

    def brith_fishes(self) -> list[Fish]:
        return [self._birth_fish() for _ in range(randint(const.MIN_FISH_TO_BIRTH, const.MAX_FISH_TO_BIRTH))]

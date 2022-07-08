from __future__ import annotations

from random import randint

from src.constants import FISH_VITALITY_SPOIL_RATE, FISH_NEED_MULTI_VITALITY_TO_BREED, EVOLUTION_DEVIATION_DIV
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class Fish(PondObject):
    def __init__(self, speed: int, size: int, pos: Position):
        super().__init__(ObjectKind.FISH, pos)
        self._speed: int = speed
        self._size: int = size
        self._vitality: int = self._speed + self._size
        self._vitality_need_to_breed: int = self._vitality * FISH_NEED_MULTI_VITALITY_TO_BREED

    @property
    def vitality(self) -> int:
        return self._vitality

    @vitality.setter
    def vitality(self, val):
        self._vitality = val

    def spoil_vitality(self) -> None:
        self._vitality -= FISH_VITALITY_SPOIL_RATE

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(randint(-self._speed, self._speed), randint(-self._speed, self._speed))

    def is_dead(self) -> bool:
        return self.vitality <= 0

    def is_breeding(self) -> bool:
        return self._vitality >= self._vitality_need_to_breed

    def calc_deviation(self, val):
        return val // EVOLUTION_DEVIATION_DIV

    def birth_fish(self) -> Fish:
        child_speed = self._speed + randint(-self.calc_deviation(self._speed), self.calc_deviation(self._speed))


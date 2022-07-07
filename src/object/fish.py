from random import randint

from src.constants import FISH_ENERGY_SPOIL_RATE
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class Fish(PondObject):
    def __init__(self, speed: int, size: int, pos: Position):
        super().__init__(ObjectKind.FISH, pos)
        self._speed: int = speed
        self._size: int = size
        self._energy: int = self._speed + self._size

    def spoil_energy(self) -> None:
        self._energy -= FISH_ENERGY_SPOIL_RATE

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(randint(-self._speed, self._speed), randint(-self._speed, self._speed))

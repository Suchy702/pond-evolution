from src.pond_object import PondObject
from src.position import Position
from random import randint

FISH_ENERGY_SPOIL = 1


class Fish(PondObject):
    def __init__(self, speed: int, size: int, pos: Position):
        super().__init__('F', pos)
        self._speed: int = speed
        self._size: int = size
        self.energy: int = self._speed + self._size

    def spoil_energy(self) -> None:
        self.energy -= FISH_ENERGY_SPOIL

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(randint(-1, 1), randint(-1, 1))

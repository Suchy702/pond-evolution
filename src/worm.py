from random import randint

from src.pond_object import PondObject
from src.position import Position


WORM_FALLING_SPEED_DIV = 15
WORM_BOUNCE_RATIO_DIV = 20


class Worm(PondObject):
    def __init__(self, energy_val: int, pos: Position, pond_dimensions: tuple[int, int]):
        super().__init__('W', pos)
        self._energy_val = energy_val
        self._falling_speed: int = max(1, pond_dimensions[0] // WORM_FALLING_SPEED_DIV)
        self._bounce_ratio: int = max(1, pond_dimensions[1] // WORM_BOUNCE_RATIO_DIV)

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(self._falling_speed, randint(-self._bounce_ratio, self._bounce_ratio))

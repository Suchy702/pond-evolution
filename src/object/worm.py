from random import randint

from src.constants import WORM_FALLING_STEPS, WORM_BOUNCE_STEPS
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class Worm(PondObject):
    def __init__(self, energy: int, pos: Position, pond_shape: tuple[int, int]):
        super().__init__(ObjectKind.WORM, pos)
        self._energy: int = energy
        self._falling_speed = max(1, pond_shape[0] // WORM_FALLING_STEPS)
        self._bounce_ratio = max(1, pond_shape[1] // WORM_BOUNCE_STEPS)

    @property
    def energy(self):
        return self._energy

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(self._falling_speed, randint(-self._bounce_ratio, self._bounce_ratio))

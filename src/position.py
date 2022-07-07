from __future__ import annotations

from dataclasses import dataclass
from random import randint


@dataclass
class Position:
    y: int
    x: int

    def changed(self, y_change: int, x_change: int) -> Position:
        return Position(self.y + y_change, self.x + x_change)

    @staticmethod
    def random_position(min_y, max_y, min_x, max_x) -> Position:
        return Position(randint(min_y, max_y), randint(min_x, max_x))

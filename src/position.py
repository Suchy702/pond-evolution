from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
    y: int
    x: int

    def changed(self, y_change: int, x_change: int) -> Position:
        return Position(self.y + y_change, self.x + x_change)

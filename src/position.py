from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
    def __init__(self, y: int, x: int):
        self.y: int = y
        self.x: int = x

    def changed(self, y_change: int, x_change: int) -> Position:
        return Position(self.y + y_change, self.x + x_change)

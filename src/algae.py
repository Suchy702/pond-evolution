from src.pond_object import PondObject
from src.position import Position

ALGAE_SURFACING_SPEED_DIV = 15


class Algae(PondObject):
    def __init__(self, energy_val: int, pos: Position, pond_height: int):
        super().__init__('A', pos)
        self._energy_val: int = energy_val
        self._surfacing_speed: int = max(1, pond_height // ALGAE_SURFACING_SPEED_DIV)

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(-self._surfacing_speed, 0)

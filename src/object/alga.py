from overrides import overrides

from src.constants import ALGA_SURFACING_STEPS
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class Alga(PondObject):
    def __init__(self, energy: int, pos: Position, pond_height: int):
        super().__init__(ObjectKind.ALGA, pos)
        self._energy: int = energy
        self._surfacing_speed: int = max(1, pond_height // ALGA_SURFACING_STEPS)

    @property
    def energy(self):
        return self._energy

    # TODO: move to update() or new class
    def find_pos_to_move(self) -> Position:
        return self.pos.changed(-self._surfacing_speed, 0)

    @overrides
    def update(self) -> None:
        pass

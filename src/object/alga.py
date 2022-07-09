from src.constants import ALGA_SURFACING_STEPS
from src.events.event_manager import EventManager
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position

event_manager = EventManager()


class Alga(PondObject):
    def __init__(self, energy_val: int, pos: Position, pond_height: int):
        super().__init__(ObjectKind.ALGA, pos)
        self._energy_val: int = energy_val
        self._surfacing_speed: int = max(1, pond_height // ALGA_SURFACING_STEPS)

    @property
    def energy_val(self) -> int:
        return self._energy_val

    def find_pos_to_move(self) -> Position:
        return self.pos.changed(-self._surfacing_speed, 0)

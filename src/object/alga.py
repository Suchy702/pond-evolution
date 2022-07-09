from src.constants import ALGA_SURFACING_STEPS
from src.events.event import Event, EventType
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
        n_pos = self.pos.changed(-self._surfacing_speed, 0)
        event_manager.emit_event(
            Event(EventType.ANIM_MOVE, object=self, from_x=self.pos.x, from_y=self.pos.y, to_x=n_pos.x, to_y=n_pos.y))
        return n_pos

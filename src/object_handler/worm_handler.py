from typing import cast

from overrides import overrides

from src.constants import WORM_ENERGY_VALUE, NUM_OF_NEW_WORMS_AT_CYCLE
from src.events.event import Event, EventType
from src.events.event_manager import EventManager
from src.object.pond_object import PondObject
from src.object.worm import Worm
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings

event_manager = EventManager()


class WormHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def worms(self):
        return [cast(Worm, worm) for worm in self.objects]

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = 0
        return Worm(WORM_ENERGY_VALUE, pos, self._pond.shape)

    def add_worms(self) -> None:
        self.add_all([self.create_random_single() for _ in range(NUM_OF_NEW_WORMS_AT_CYCLE)])

    def move_worms(self) -> None:
        for worm in self.worms:
            n_pos = self._pond.trim_position(worm.find_pos_to_move())
            event_manager.emit_event(
                Event(EventType.ANIM_MOVE, object=worm, from_x=worm.pos.x, from_y=worm.pos.y, to_x=n_pos.x,
                      to_y=n_pos.y))
            self._pond.change_position(worm, n_pos)

    def remove_worms_on_the_ground(self) -> None:
        self.remove_all([worm for worm in self.worms if self._pond.is_on_ground(worm.pos)])

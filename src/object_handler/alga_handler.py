from typing import cast

from overrides import overrides

from src.constants import ALGA_ENERGY_VALUE
from src.events.event import Event, EventType
from src.events.event_manager import EventManager
from src.object.alga import Alga
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings

event_manager = EventManager()


class AlgaHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def algae(self):
        return [cast(Alga, alga) for alga in self.objects]

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        return Alga(ALGA_ENERGY_VALUE, pos, self._pond.height)

    def move_algae(self) -> None:
        for algae in self.algae:
            n_pos = self._pond.trim_position(algae.find_pos_to_move())
            event_manager.emit_event(
                Event(EventType.ANIM_MOVE, object=algae, from_x=algae.pos.x, from_y=algae.pos.y, to_x=n_pos.x,
                      to_y=n_pos.y))
            self._pond.change_position(algae, n_pos)

    def remove_algae_on_surface(self) -> None:
        self.remove_all([alga for alga in self.algae if self._pond.is_on_surface(alga.pos)])

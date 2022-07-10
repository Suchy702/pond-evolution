from itertools import chain
from typing import cast

from overrides import overrides

from src.events.event import Event, EventType
from src.events.event_manager.event_manager import EventManager
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings

event_manager = EventManager()


class AlgaMakerHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def alga_makers(self):
        return [cast(AlgaMaker, alga_maker) for alga_maker in self.objects]

    def move_alga_maker(self) -> None:
        for alga_maker in self.alga_makers:
            event_manager.emit_event(
                Event(EventType.ANIM_STAY, object=alga_maker, x=alga_maker.pos.x, y=alga_maker.pos.y))

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = self._pond.height - 1
        return AlgaMaker(pos, self._pond.height)

    def create_algae(self) -> list[Alga]:
        return list(chain.from_iterable([alga_maker.create_algae(self._pond) for alga_maker in self.alga_makers]))

from typing import cast

from overrides import overrides

from src.constants import ALGA_ENERGY_VALUE
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.events.event_type import GraphicEventType
from src.object.alga import Alga
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.object_kind import ObjectKind
from src.position import Position
from src.simulation_settings import SimulationSettings

event_emitter = EventEmitter()


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

    def handle_decisions(self, decisions: DecisionSet) -> None:
        for decision in decisions[DecisionType.MOVE, ObjectKind.ALGA]:
            self.move_alga(decision)

    def move_alga(self, decision: Decision) -> None:
        n_pos = self._pond.trim_position(Position(decision.to_y, decision.to_x))
        event_emitter.emit_event(
            GraphicEvent(
                GraphicEventType.ANIM_MOVE, pond_object=decision.pond_object,
                from_x=decision.pond_object.pos.x, from_y=decision.pond_object.pos.y,
                to_x=n_pos.x, to_y=n_pos.y
            )
        )
        self._pond.change_position(decision.pond_object, n_pos)

    def remove_algae_on_surface(self) -> None:
        self.remove_all([alga for alga in self.algae if self._pond.is_on_surface(alga.pos)])

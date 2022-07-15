from typing import cast

from overrides import overrides

from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.events.event_type import GraphicEventType
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings

event_emitter = EventEmitter()


class AlgaMakerHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def alga_makers(self):
        return [cast(AlgaMaker, alga_maker) for alga_maker in self.objects]

    def handle_decisions(self, decisions: DecisionSet):
        for decision in decisions[DecisionType.STAY, ObjectKind.ALGA_MAKER]:
            self.move_alga_maker(decision)

    def move_alga_maker(self, decision: Decision) -> None:
        event_emitter.emit_event(
            GraphicEvent(
                GraphicEventType.ANIM_STAY, pond_object=decision.pond_object,
                x=decision.pond_object.pos.x, y=decision.pond_object.pos.y
            )
        )

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = self._pond.height - 1
        return AlgaMaker(pos, self._pond.height)

    def create_algae(self, algae_maker: AlgaMaker) -> list[Alga]:
        return algae_maker.create_algae(self._pond)

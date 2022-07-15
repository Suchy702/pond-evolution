from typing import cast

from overrides import overrides

from src.constants import WORM_ENERGY_VALUE, NUM_OF_NEW_WORMS_AT_CYCLE
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.events.event_type import GraphicEventType
from src.object.pond_object import PondObject
from src.object.worm import Worm
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.object_kind import ObjectKind
from src.position import Position
from src.simulation_settings import SimulationSettings

event_emitter = EventEmitter()


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

    def handle_decisions(self, decisions: DecisionSet):
        for decision in decisions[DecisionType.MOVE, ObjectKind.WORM]:
            self.move_worm(decision)
        if decisions[DecisionType.REPRODUCE, ObjectKind.WORM]:
            self.add_worms()

    def move_worm(self, decision: Decision) -> None:
        n_pos = self._pond.trim_position(Position(decision.to_y, decision.to_x))
        event_emitter.emit_event(
            GraphicEvent(GraphicEventType.ANIM_MOVE, pond_object=decision.pond_object,
                         from_x=decision.pond_object.pos.x, from_y=decision.pond_object.pos.y,
                         to_x=n_pos.x, to_y=n_pos.y
                         )
        )
        self._pond.change_position(decision.pond_object, n_pos)

    def add_worms(self) -> None:
        self.add_all([self.create_random_single() for _ in range(NUM_OF_NEW_WORMS_AT_CYCLE)])

    def remove_worms_on_the_ground(self) -> None:
        self.remove_all([worm for worm in self.worms if self._pond.is_on_ground(worm.pos)])

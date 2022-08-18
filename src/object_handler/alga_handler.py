from typing import cast

from overrides import overrides

from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.alga import Alga
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.position import Position
from src.simulation_settings import SimulationSettings


class AlgaHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def algae(self) -> list[Alga]:
        objects = cast(list[Alga], self.objects)
        return objects

    @overrides
    def create_random_single(self) -> PondObject:
        position = self._pond.random_position()
        return Alga(self.settings.alga_energy, position, self._pond.height)

    def handle_decisions(self, decisions: DecisionSet) -> None:
        for decision in decisions[DecisionType.MOVE, ObjectKind.ALGA]:
            self.move_alga(decision)

    def move_alga(self, decision: Decision) -> None:
        new_position = self._pond.trim_position(Position(decision.to_y, decision.to_x))
        self.event_emitter.emit_anim_move_event(decision, new_position)
        self._pond.change_position(decision.pond_object, new_position)

    def remove_algae_on_surface(self) -> None:
        self.remove_all([alga for alga in self.algae if self._pond.is_on_surface(alga.position)])

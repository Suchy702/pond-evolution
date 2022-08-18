from typing import TYPE_CHECKING

from overrides import overrides

from src.ai.ai import AI
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.pond.pond_viewer import PondViewer
from src.position import Position

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from src.object.alga import Alga


class AlgaAI(AI["Alga"]):
    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        decisions = DecisionSet()
        decisions.add(self._movement_decision())
        return decisions

    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(-self.pond_object.surfacing_speed, 0)

    def _movement_decision(self) -> Decision:
        pos_to_move = self._find_pos_to_move()
        return Decision(DecisionType.MOVE, pond_object=self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y)

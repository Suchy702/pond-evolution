from overrides import overrides

from src.ai.ai import AI
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.position import Position


class AlgaAI(AI["Alga"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(-self.pond_object.surfacing_speed, 0)

    def _movement_decision(self, decisions: DecisionSet) -> None:
        pos_to_move = self._find_pos_to_move()
        decisions.add(Decision(
            DecisionType.MOVE, pond_object=self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y
        ))

    @overrides
    def get_decisions(self) -> DecisionSet:
        decisions = DecisionSet()
        self._movement_decision(decisions)
        return decisions

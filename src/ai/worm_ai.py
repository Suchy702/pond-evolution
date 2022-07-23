from random import randint, random

from overrides import overrides

from src.ai.ai import AI
from src.constants import CHANCE_TO_PRODUCE_WORMS
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object_kind import ObjectKind
from src.pond_viewer import PondViewer
from src.position import Position


class WormAI(AI["Worm"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(
            self.pond_object.falling_speed,
            randint(-self.pond_object.bounce_ratio, self.pond_object.bounce_ratio)
        )

    def _movement_decision(self, decisions: DecisionSet):
        pos_to_move = self._find_pos_to_move()
        decisions.add(Decision(
            DecisionType.MOVE, pond_object=self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y
        ))

    @staticmethod
    def _reproduce_decision(decisions: DecisionSet):
        if random() < CHANCE_TO_PRODUCE_WORMS / 100:
            decisions.add(Decision(DecisionType.REPRODUCE, kind=ObjectKind.WORM))

    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        decisions = DecisionSet()
        self._movement_decision(decisions)
        return decisions

    @staticmethod
    def get_general_decisions() -> DecisionSet:
        decisions = DecisionSet()
        WormAI._reproduce_decision(decisions)
        return decisions

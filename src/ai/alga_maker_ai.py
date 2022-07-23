from random import random

from overrides import overrides

from src.ai.ai import AI
from src.constants import CHANCE_TO_PRODUCE_ALGAE
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType


class AlgaMakerAI(AI["AlgaMaker"]):
    def _movement_decision(self, decisions: DecisionSet) -> None:
        decisions.add(Decision(
            DecisionType.STAY, pond_object=self.pond_object, to_x=self.pond_object.pos.x, to_y=self.pond_object.pos.y
        ))

    def _reproduce_decision(self, decisions: DecisionSet) -> None:
        if random() < CHANCE_TO_PRODUCE_ALGAE / 100:
            decisions.add(Decision(DecisionType.REPRODUCE, pond_object=self.pond_object))

    @overrides
    def get_decisions(self) -> DecisionSet:
        decisions = DecisionSet()
        self._movement_decision(decisions)
        self._reproduce_decision(decisions)
        return decisions

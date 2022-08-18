from random import random
from typing import Optional, TYPE_CHECKING

from overrides import overrides

from src.ai.ai import AI
from src.constants import CHANCE_TO_PRODUCE_ALGAE
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.pond.pond_viewer import PondViewer

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from src.object.alga_maker import AlgaMaker


class AlgaMakerAI(AI["AlgaMaker"]):
    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        decisions = DecisionSet()
        decisions.add(self._movement_decision())
        decisions.add(self._reproduce_decision())
        return decisions

    def _movement_decision(self) -> Decision:
        to_x, to_y = self.pond_object.pos.x, self.pond_object.pos.y
        return Decision(DecisionType.STAY, pond_object=self.pond_object, to_x=to_x, to_y=to_y)

    def _reproduce_decision(self) -> Optional[Decision]:
        if random() < CHANCE_TO_PRODUCE_ALGAE:
            return Decision(DecisionType.REPRODUCE, pond_object=self.pond_object)
        return None

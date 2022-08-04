from random import randint, random
from typing import Optional, TYPE_CHECKING

from overrides import overrides

from src.ai.ai import AI
from src.constants import CHANCE_TO_PRODUCE_WORMS
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.object_kind import ObjectKind
from src.pond.pond_viewer import PondViewer
from src.position import Position

if TYPE_CHECKING:
    pass


class WormAI(AI["Worm"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(
            self.pond_object.falling_speed,
            randint(-self.pond_object.bounce_ratio, self.pond_object.bounce_ratio)
        )

    def _movement_decision(self) -> Decision:
        pos_to_move = self._find_pos_to_move()
        return Decision(DecisionType.MOVE, pond_object=self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y)

    @staticmethod
    def _reproduce_decision() -> Optional[Decision]:
        if random() < CHANCE_TO_PRODUCE_WORMS / 100:
            return Decision(DecisionType.REPRODUCE, kind=ObjectKind.WORM)
        return None

    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        decisions = DecisionSet()
        decisions.add(self._movement_decision())
        return decisions

    @staticmethod
    def get_general_decisions() -> DecisionSet:
        decisions = DecisionSet()
        decisions.add(WormAI._reproduce_decision())
        return decisions

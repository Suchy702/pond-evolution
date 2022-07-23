from random import randint

from overrides import overrides

from src.ai.ai import AI
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.fish_trait import FishTrait
from src.pond_viewer import PondViewer
from src.position import Position


class FishAI(AI["Fish"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(
            randint(-self.pond_object.speed, self.pond_object.speed),
            randint(-self.pond_object.speed, self.pond_object.speed)
        )

    def _movement_decision(self, decisions: DecisionSet) -> None:
        if FishTrait.PREDATOR in self.pond_object.traits:
            decisions.add(Decision(
                DecisionType.STAY, pond_object=self.pond_object, to_x=self.pond_object.pos.x,
                to_y=self.pond_object.pos.y
            ))
        else:
            pos_to_move = self._find_pos_to_move()
            decisions.add(Decision(
                DecisionType.MOVE, pond_object=self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y
            ))

    def _reproduce_decision(self, decisions: DecisionSet) -> bool:
        if self.pond_object.vitality > self.pond_object.vitality_need_to_breed:
            decisions.add(Decision(DecisionType.REPRODUCE, pond_object=self.pond_object))
            return True
        return False

    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        decisions = DecisionSet()
        is_dead = self._reproduce_decision(decisions)
        if not is_dead:
            self._movement_decision(decisions)
        return decisions

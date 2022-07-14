from abc import ABC, abstractmethod
from random import randint
from typing import TypeVar, Generic

from overrides import overrides

from src.decision.decision import decisionSetType, Decision
from src.decision.decision_type import DecisionType
from src.object.pond_object import PondObject
from src.position import Position

T = TypeVar('T', bound=PondObject)


class AI(ABC, Generic[T]):
    def __init__(self, pond_object: T):
        self.pond_object = pond_object

    @abstractmethod
    def get_decisions(self) -> decisionSetType:
        pass


class FishAI(AI["Fish"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(randint(-self.pond_object.speed, self.pond_object.speed),
                                            randint(-self.pond_object.speed, self.pond_object.speed))

    def _movement_decision(self, decisions: decisionSetType):
        pos_to_move = self._find_pos_to_move()
        Decision(DecisionType.MOVE, self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y).add_to_dict(decisions)

    def _breed_decision(self, decisions: decisionSetType):
        if self.pond_object.vitality > self.pond_object.vitality_need_to_breed:
            Decision(DecisionType.BREED, self.pond_object).add_to_dict(decisions)

    @overrides
    def get_decisions(self) -> decisionSetType:
        decisions = {}
        self._movement_decision(decisions)
        self._breed_decision(decisions)
        return decisions


class WormAI(AI["Worm"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(self.pond_object.falling_speed,
                                            randint(-self.pond_object.bounce_ratio, self.pond_object.bounce_ratio))

    def _movement_decision(self, decisions: decisionSetType):
        pos_to_move = self._find_pos_to_move()
        Decision(DecisionType.MOVE, self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y).add_to_dict(decisions)

    @overrides
    def get_decisions(self) -> decisionSetType:
        decisions = {}
        self._movement_decision(decisions)
        return decisions


class AlgaAI(AI["Alga"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(-self.pond_object.surfacing_speed, 0)

    def _movement_decision(self, decisions: decisionSetType):
        pos_to_move = self._find_pos_to_move()
        Decision(DecisionType.MOVE, self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y).add_to_dict(decisions)

    @overrides
    def get_decisions(self) -> decisionSetType:
        decisions = {}
        self._movement_decision(decisions)
        return decisions


class AlgaMakerAI(AI["AlgaMaker"]):
    def _movement_decision(self, decisions: decisionSetType):
        Decision(DecisionType.STAY, self.pond_object, to_x=self.pond_object.pos.x,
                 to_y=self.pond_object.pos.y).add_to_dict(decisions)

    @overrides
    def get_decisions(self) -> decisionSetType:
        decisions = {}
        self._movement_decision(decisions)
        return decisions

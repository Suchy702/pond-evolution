from abc import ABC, abstractmethod
from random import randint, random
from typing import TypeVar, Generic

from overrides import overrides

from src.constants import CHANCE_TO_PRODUCE_ALGAE, CHANCE_TO_PRODUCE_WORMS
from src.decision.decision import decisionSetType, Decision
from src.decision.decision_type import DecisionType
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position

T = TypeVar('T', bound=PondObject)


class AI(ABC, Generic[T]):
    def __init__(self, pond_object: T):
        self.pond_object = pond_object

    @abstractmethod
    def get_decisions(self) -> decisionSetType:
        pass

    @staticmethod
    def get_general_decisions() -> decisionSetType:
        return {}


class FishAI(AI["Fish"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(randint(-self.pond_object.speed, self.pond_object.speed),
                                            randint(-self.pond_object.speed, self.pond_object.speed))

    def _movement_decision(self, decisions: decisionSetType):
        pos_to_move = self._find_pos_to_move()
        Decision(DecisionType.MOVE, self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y).add_to_dict(decisions)

    def _reproduce_decision(self, decisions: decisionSetType):
        if self.pond_object.vitality > self.pond_object.vitality_need_to_breed:
            Decision(DecisionType.REPRODUCE, self.pond_object).add_to_dict(decisions)

    @overrides
    def get_decisions(self) -> decisionSetType:
        decisions = {}
        self._movement_decision(decisions)
        self._reproduce_decision(decisions)
        return decisions


class WormAI(AI["Worm"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(self.pond_object.falling_speed,
                                            randint(-self.pond_object.bounce_ratio, self.pond_object.bounce_ratio))

    def _movement_decision(self, decisions: decisionSetType):
        pos_to_move = self._find_pos_to_move()
        Decision(DecisionType.MOVE, self.pond_object, to_x=pos_to_move.x, to_y=pos_to_move.y).add_to_dict(decisions)

    @staticmethod
    def _reproduce_decision(decisions: decisionSetType):
        if random() < CHANCE_TO_PRODUCE_ALGAE / 100:
            Decision(DecisionType.REPRODUCE, None, kind=ObjectKind.WORM).add_to_dict(decisions)

    @overrides
    def get_decisions(self) -> decisionSetType:
        decisions = {}
        self._movement_decision(decisions)
        self._reproduce_decision(decisions)
        return decisions

    @staticmethod
    def get_general_decisions() -> decisionSetType:
        decisions = {}
        WormAI._reproduce_decision(decisions)
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

    def _reproduce_decision(self, decisions: decisionSetType):
        if random() < CHANCE_TO_PRODUCE_WORMS / 100:
            Decision(DecisionType.REPRODUCE, self.pond_object).add_to_dict(decisions)

    @overrides
    def get_decisions(self) -> decisionSetType:
        decisions = {}
        self._movement_decision(decisions)
        self._reproduce_decision(decisions)
        return decisions

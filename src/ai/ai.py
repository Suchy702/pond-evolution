from abc import ABC, abstractmethod
from random import randint, random
from typing import TypeVar, Generic

from overrides import overrides

from src.constants import CHANCE_TO_PRODUCE_ALGAE, CHANCE_TO_PRODUCE_WORMS
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position

T = TypeVar('T', bound=PondObject)


class AI(ABC, Generic[T]):
    def __init__(self, pond_object: T):
        self.pond_object = pond_object

    @abstractmethod
    def get_decisions(self) -> DecisionSet:
        pass

    @staticmethod
    def get_general_decisions() -> DecisionSet:
        return DecisionSet()


class FishAI(AI["Fish"]):
    def _find_pos_to_move(self) -> Position:
        return self.pond_object.pos.changed(
            randint(-self.pond_object.speed, self.pond_object.speed),
            randint(-self.pond_object.speed, self.pond_object.speed)
        )

    def _movement_decision(self, decisions: DecisionSet) -> None:
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
    def get_decisions(self) -> DecisionSet:
        decisions = DecisionSet()
        is_dead = self._reproduce_decision(decisions)
        if not is_dead:
            self._movement_decision(decisions)
        return decisions


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
    def get_decisions(self) -> DecisionSet:
        decisions = DecisionSet()
        self._movement_decision(decisions)
        return decisions

    @staticmethod
    def get_general_decisions() -> DecisionSet:
        decisions = DecisionSet()
        WormAI._reproduce_decision(decisions)
        return decisions


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

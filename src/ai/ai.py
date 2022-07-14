from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from overrides import overrides

from src.decision.decision import decisionSetType
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.fish import Fish
from src.object.pond_object import PondObject
from src.object.worm import Worm

T = TypeVar('T', bound=PondObject)


class AI(ABC, Generic[T]):
    @abstractmethod
    def get_decisions(self, objects: list[T]) -> decisionSetType:
        pass


class FishAI(AI[Fish]):
    @overrides
    def get_decisions(self, objects: list[Fish]) -> decisionSetType:
        pass


class WormAI(AI[Worm]):
    @overrides
    def get_decisions(self, objects: list[Worm]) -> decisionSetType:
        pass


class AlgaAI(AI[Alga]):
    @overrides
    def get_decisions(self, objects: list[Fish]) -> decisionSetType:
        pass


class AlgaMakerAI(AI[AlgaMaker]):
    @overrides
    def get_decisions(self, objects: list[Fish]) -> decisionSetType:
        pass

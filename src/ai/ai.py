from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from overrides import overrides

from src.decision.decision import decisionSetType
from src.object.pond_object import PondObject

T = TypeVar('T', bound=PondObject)


class AI(ABC, Generic[T]):
    def __init__(self, pond_object: T):
        self.pond_object = pond_object

    @abstractmethod
    def get_decisions(self) -> decisionSetType:
        pass


class FishAI(AI["Fish"]):
    @overrides
    def get_decisions(self) -> decisionSetType:
        pass


class WormAI(AI["Worm"]):
    @overrides
    def get_decisions(self) -> decisionSetType:
        pass


class AlgaAI(AI["Alga"]):
    @overrides
    def get_decisions(self) -> decisionSetType:
        pass


class AlgaMakerAI(AI["AlgaMaker"]):
    @overrides
    def get_decisions(self) -> decisionSetType:
        pass

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.decision.decision_set import DecisionSet
from src.object.pond_object import PondObject
from src.pond_viewer import PondViewer

T = TypeVar('T', bound=PondObject)


class AI(ABC, Generic[T]):
    def __init__(self, pond_object: T):
        self.pond_object = pond_object

    @abstractmethod
    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        pass

    @staticmethod
    def get_general_decisions() -> DecisionSet:
        return DecisionSet()

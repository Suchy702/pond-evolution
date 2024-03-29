from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from src.decision.decision_set import DecisionSet
from src.object.object_kind import ObjectKind
from src.pond.pond_viewer import PondViewer
from src.position import Position

if TYPE_CHECKING:
    from src.ai.ai import AI


class PondObject(ABC):
    def __init__(self, object_kind: ObjectKind, position: Position, ai: AI):
        self._id: int = -1
        self._kind: ObjectKind = object_kind
        self.position: Position = position
        self._energy_value: int = 0
        self.ai = ai

    @property
    def energy_value(self) -> int:
        return self._energy_value

    @property
    def kind(self) -> ObjectKind:
        return self._kind

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id_: int):
        if self._id != -1:
            raise Exception("ID already set!")
        self._id = id_

    def get_decisions(self, pond_viewer: PondViewer) -> DecisionSet:
        return self.ai.get_decisions(pond_viewer)

    def __str__(self):
        return f'{self._kind}-{self._id}'

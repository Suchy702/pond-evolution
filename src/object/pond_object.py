from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from src.decision.decision import decisionSetType
from src.object_kind import ObjectKind
from src.position import Position

if TYPE_CHECKING:
    from src.ai.ai import AI


class PondObject(ABC):
    def __init__(self, obj_kind: ObjectKind, obj_pos: Position, ai: AI):
        self._id: int = -1
        self._kind: ObjectKind = obj_kind
        self.pos: Position = obj_pos
        self._energy_val: int = 0
        self.ai = ai

    @property
    def energy_val(self) -> int:
        return self._energy_val

    @property
    def kind(self) -> ObjectKind:
        return self._kind

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id_):
        if self._id != -1:
            raise Exception("ID already set!")
        self._id = id_

    def get_decisions(self) -> decisionSetType:
        return self.ai.get_decisions()

    def __str__(self):
        return f'{self._kind}-{self._id}'

from src.object_kind import ObjectKind
from src.position import Position
from abc import ABC


class PondObject(ABC):
    def __init__(self, obj_kind: ObjectKind, obj_pos: Position):
        self._id: int = -1
        self._kind: ObjectKind = obj_kind
        self.pos: Position = obj_pos

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

    def __str__(self):
        return f'{self._kind}-{self._id}'

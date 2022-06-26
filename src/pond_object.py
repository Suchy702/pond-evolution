from src.position import Position
from abc import ABC


class PondObject(ABC):
    def __init__(self, obj_kind: str, obj_pos: Position):
        self._id: int = -1
        self._kind: str = obj_kind
        self.pos: Position = obj_pos

    @property
    def kind(self):
        return self._kind

    @property
    def id(self):
        return self._id

    def set_id(self, id_):
        if self._id != -1:
            raise Exception("Id already setted!")
        self._id = id_

    def __str__(self):
        return self._kind + str(self._id)

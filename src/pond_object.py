from src.position import Position
from abc import ABC


class PondObject(ABC):
    def __init__(self, obj_kind: str, obj_pos: Position):
        self._id: int = -1
        self._kind: str = obj_kind
        self.pos: Position = obj_pos
        self.energy_val: int = 0

    @property
    def kind(self):
        return self._kind

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        if self._id != -1:
            raise Exception("ID already set!")
        self._id = id_

    def __str__(self):
        return f'{self._kind}{self._id}'

from random import randint

from src.pond_object import PondObject
from src.position import Position


class Pond:
    def __init__(self, height: int, width: int):
        self._height: int = height
        self._width: int = width
        self._pond: list[list[set[PondObject]]] = [[set() for _ in range(self._width)] for _ in range(self._height)]

    @property
    def dimensions(self):
        return self._height, self._width

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def get_spot(self, pos: Position) -> set[PondObject]:
        return self._pond[pos.y][pos.x]

    def get_row(self, row_idx: int):
        return self._pond[row_idx]

    def add(self, obj: PondObject) -> None:
        if obj in self.get_spot(obj.pos):
            raise Exception("Object already in Spot!")
        self.get_spot(obj.pos).add(obj)

    def remove(self, obj: PondObject) -> None:
        if obj not in self.get_spot(obj.pos):
            raise Exception("Object not in Spot!")
        self.get_spot(obj.pos).remove(obj)

    def change_pos(self, obj: PondObject, new_pos: Position) -> None:
        self.remove(obj)
        obj.pos = new_pos
        self.add(obj)

    def correct_pos(self, pos: Position) -> Position:
        return Position(min(self._height-1, max(0, pos.y)), min(self._width-1, max(0, pos.x)))

    def random_pos(self) -> Position:
        return Position(randint(0, self._height-1), randint(0, self._width-1))

    def is_on_the_ground(self, pos: Position) -> bool:
        return pos.y == self.height-1

    @staticmethod
    def is_on_surface(pos: Position) -> bool:
        return pos.y == 0

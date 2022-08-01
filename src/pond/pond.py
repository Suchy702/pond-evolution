from src.object.pond_object import PondObject
from src.position import Position
from src.simulation_settings import SimulationSettings


class Pond:
    def __init__(self, settings: SimulationSettings):
        self._height: int = settings.pond_height
        self._width: int = settings.pond_width
        self._pond: list[list[set[PondObject]]] = [[set() for _ in range(self._width)] for _ in range(self._height)]

    @property
    def shape(self) -> tuple[int, int]:
        return self._height, self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def get_spot(self, pos: Position) -> set[PondObject]:
        return self._pond[pos.y][pos.x]

    def get_row(self, row_idx: int) -> list[set[PondObject]]:
        return self._pond[row_idx]

    def add(self, obj: PondObject) -> None:
        if obj in self.get_spot(obj.pos):
            raise Exception("Object already in that spot!")

        self.get_spot(obj.pos).add(obj)

    def remove(self, obj: PondObject) -> None:
        spot = self.get_spot(obj.pos)
        if obj not in spot:
            raise Exception("No object in that spot!")

        self.get_spot(obj.pos).remove(obj)

    def change_position(self, obj: PondObject, new_pos: Position) -> None:
        self.remove(obj)
        obj.pos = new_pos
        self.add(obj)

    def trim_position(self, pos: Position) -> Position:
        return Position(min(self._height - 1, max(0, pos.y)), min(self._width - 1, max(0, pos.x)))

    def random_position(self) -> Position:
        return Position.random_position(0, self.height - 1, 0, self._width - 1)

    def is_on_ground(self, pos: Position) -> bool:
        return pos.y == self.height - 1

    @staticmethod
    def is_on_surface(pos: Position) -> bool:
        return pos.y == 0

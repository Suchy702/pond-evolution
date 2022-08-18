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

    def get_spot(self, position: Position) -> set[PondObject]:
        return self._pond[position.y][position.x]

    def get_row(self, row_idx: int) -> list[set[PondObject]]:
        return self._pond[row_idx]

    def add(self, object_: PondObject) -> None:
        if object_ in self.get_spot(object_.position):
            raise Exception("Object already in that spot!")

        self.get_spot(object_.position).add(object_)

    def remove(self, object_: PondObject) -> None:
        if object_ not in self.get_spot(object_.position):
            raise Exception("No object in that spot!")

        self.get_spot(object_.position).remove(object_)

    def change_position(self, object_: PondObject, new_position: Position) -> None:
        self.remove(object_)
        object_.position = new_position
        self.add(object_)

    def trim_position(self, position: Position) -> Position:
        return Position(min(self._height - 1, max(0, position.y)), min(self._width - 1, max(0, position.x)))

    def random_position(self) -> Position:
        return Position.random_position(0, self.height - 1, 0, self._width - 1)

    def is_on_ground(self, position: Position) -> bool:
        return position.y == self.height - 1

    @staticmethod
    def is_on_surface(position: Position) -> bool:
        return position.y == 0

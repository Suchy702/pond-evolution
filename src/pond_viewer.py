from __future__ import annotations

from typing import Callable, cast, TYPE_CHECKING

from src.position import Position

if TYPE_CHECKING:
    from src.object.fish import Fish
    from src.object.fish_trait import FishTrait
    from src.object.pond_object import PondObject
    from src.object_kind import ObjectKind
    from src.pond import Pond


class PondViewer:
    def __init__(self, pond_width: int, pond_height: int, *ponds: Pond):
        self.ponds: list[Pond] = list(ponds)
        self.pond_width = pond_width
        self.pond_height = pond_height

    def add_pond(self, pond: Pond) -> None:
        self.ponds.append(pond)

    def add_ponds(self, ponds: list[Pond]) -> None:
        for pond in ponds:
            self.add_pond(pond)

    def get_visible_objects(self, pos: Position, eyesight: int) -> list[PondObject]:
        return self._get_visible_objects(pos, eyesight, lambda obj: True)

    def get_visible_object_by_type(self, pos: Position, eyesight: int, obj_type: list[ObjectKind]) -> list[PondObject]:
        return self._get_visible_objects(pos, eyesight, lambda obj: obj.kind in obj_type)

    def get_visible_object_by_trait(self, pos: Position, eyesight: int, traits: list[FishTrait]) -> list[Fish]:
        fish = self.get_visible_object_by_type(pos, eyesight, [ObjectKind.FISH])
        n_list = []
        for f in fish:
            f = cast(Fish, f)
            if any(trait in traits for trait in f.traits):
                n_list.append(f)

        return n_list

    def _get_visible_objects(self, pos: Position, eyesight: int, obj_filter: Callable[[PondObject], bool]) -> list[
        PondObject]:
        objects = []
        x_coor = self._get_x_coordinates(pos.x, eyesight)
        for x in range(x_coor[0], x_coor[1] + 1):
            y_coor = self._get_y_coordinates(pos.y, eyesight - abs(x - pos.x))
            for y in range(y_coor[0], y_coor[1] + 1):
                for pond in self.ponds:
                    for obj in pond.get_spot(Position(y, x)):
                        if obj_filter(obj):
                            objects.append(obj)
        return objects

    def _get_x_coordinates(self, x: int, radius: int) -> tuple[int, int]:
        return max(0, x - radius + 1), min(self.pond_width - 1, x + radius - 1)

    def _get_y_coordinates(self, y: int, radius: int) -> tuple[int, int]:
        return max(0, y - radius + 1), min(self.pond_height - 1, y + radius - 1)

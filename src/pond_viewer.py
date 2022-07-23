from __future__ import annotations

import itertools
from typing import Callable, cast, TYPE_CHECKING, Optional, Generator

from src.object_kind import ObjectKind
from src.position import Position

if TYPE_CHECKING:
    from src.object.fish import Fish
    from src.object.fish_trait import FishTrait
    from src.object.pond_object import PondObject
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

    def get_visible_objects(self, pos: Position, eyesight: int) -> Generator[list[PondObject], None, None]:
        yield from self._get_visible_objects(pos, eyesight, lambda obj: True)

    def get_visible_object_by_type(
            self, pos: Position, eyesight: int, obj_type: list[ObjectKind], inverse: bool = False
    ) -> Generator[list[PondObject]]:
        yield from self._get_visible_objects(pos, eyesight, lambda obj: obj.kind in obj_type, inverse)

    def get_visible_object_by_trait(
            self, pos: Position, eyesight: int, traits: list[FishTrait], inverse: bool = False
    ) -> Generator[list[Fish]]:
        for fish_layer in self.get_visible_object_by_type(pos, eyesight, [ObjectKind.FISH], inverse):
            new_list = []
            for fish in fish_layer:
                fish = cast(Fish, fish)
                if any(trait in traits for trait in fish.traits):
                    new_list.append(fish)
            if new_list:
                yield new_list

    def _get_visible_objects(
            self, pos: Position, eyesight: int, obj_filter: Callable[[PondObject], bool], inverse: bool
    ) -> Generator[list[PondObject], None, None]:
        """Returns visible objects grouped by distance from `pos`. Groups are sorted in ascending order of distance"""
        offset = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for radius in range(eyesight):
            objects = []
            if radius == 0:
                yield self._get_spot_objects(pos, obj_filter, inverse)
                continue

            for (off_x, off_y) in offset:
                point = Position(pos.y + off_y * radius, pos.x + off_x * radius)
                if 0 <= point.x < self.pond_width and 0 <= point.y < self.pond_height:
                    objects.extend(self._get_spot_objects(point, obj_filter, inverse))

            if radius == 1:
                if objects:
                    yield objects
                continue

            for p1, p2 in itertools.pairwise(offset + [(0, 1)]):
                x_change = p2[0] - p1[0]
                y_change = p2[1] - p1[1]
                p1 = Position(pos.y + p1[1] * radius + y_change, pos.x + p1[0] * radius + x_change)
                p2 = Position(pos.y + p2[1] * radius - y_change, pos.x + p2[0] * radius - x_change)

                (first_idx, last_idx) = self._get_intersection_indices(p1, p2)

                if first_idx is None:
                    continue

                for i in range(first_idx, last_idx + 1):
                    objects.extend(self._get_spot_objects(
                        Position(p1.y + y_change * i, p1.x + x_change * i),
                        obj_filter,
                        inverse
                    ))

            if objects:
                yield objects

    def _get_intersection_indices(self, p1, p2) -> tuple[Optional[int], Optional[int]]:
        x_swapped, y_swapped = False, False
        if p1.x > p2.x:
            p1.x, p2.x = p2.x, p1.x
            x_swapped = True
        if p1.y > p2.y:
            p1.y, p2.y = p2.y, p1.y
            y_swapped = True

        x_range = self._get_intersection(p1.x, p2.x, 0, self.pond_width - 1)
        y_range = self._get_intersection(p1.y, p2.y, 0, self.pond_height - 1)

        if x_range[0] > x_range[1] or y_range[0] > y_range[1]:
            return None, None

        if x_swapped:
            p1.x, p2.x = p2.x, p1.x
        if y_swapped:
            p1.y, p2.y = p2.y, p1.y

        x_indices = [abs(x_range[0] - p1.x), abs(x_range[1] - p1.x)]
        y_indices = [abs(y_range[0] - p1.y), abs(y_range[1] - p1.y)]

        if x_indices[0] > x_indices[1]:
            x_indices[0], x_indices[1] = x_indices[1], x_indices[0]

        if y_indices[0] > y_indices[1]:
            y_indices[0], y_indices[1] = y_indices[1], y_indices[0]

        indices = self._get_intersection(x_indices[0], x_indices[1], y_indices[0], y_indices[1])
        if indices[0] > indices[1]:
            return None, None

        return indices

    @staticmethod
    def _get_intersection(a1, a2, b1, b2):
        """Returns intersection of segment [a1, a2] with [b1, b2]"""
        return max(a1, b1), min(a2, b2)

    def _get_spot_objects(self, pos: Position, obj_filter: Callable[[PondObject], bool], inverse: bool) -> list[
        PondObject]:
        objects = []
        for pond in self.ponds:
            for obj in pond.get_spot(pos):
                if (inverse and not obj_filter(obj)) or (not inverse and obj_filter(obj)):
                    objects.append(obj)
        return objects

    def _get_x_coordinates(self, x: int, radius: int) -> tuple[int, int]:
        return max(0, x - radius + 1), min(self.pond_width - 1, x + radius - 1)

    def _get_y_coordinates(self, y: int, radius: int) -> tuple[int, int]:
        return max(0, y - radius + 1), min(self.pond_height - 1, y + radius - 1)

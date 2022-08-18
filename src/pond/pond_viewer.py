from __future__ import annotations

import itertools
from typing import Callable, cast, TYPE_CHECKING, Optional, Generator

from src.object.object_kind import ObjectKind
from src.position import Position

if TYPE_CHECKING:
    from src.object.fish import Fish
    from src.object.fish_trait import FishTrait
    from src.object.pond_object import PondObject
    from src.pond.pond import Pond


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

    def get_visible_objects(self, position: Position, eyesight: int) -> Generator[list[PondObject], None, None]:
        yield from self._get_visible_objects(position, eyesight, lambda _: True)

    def get_visible_objects_by_type(
            self, position: Position, eyesight: int, object_type: list[ObjectKind], negate: bool = False
    ) -> Generator[list[PondObject], None, None]:
        """
        If negate is false return objects of one of the types specified in `obj_type`. Otherwise, return objects whose
        type is not in `obj_type`.
        """
        yield from self._get_visible_objects(position, eyesight, lambda object_: object_.kind in object_type, negate)

    def get_visible_object_by_trait(
            self, position: Position, eyesight: int, traits: list[FishTrait], negate: bool = False
    ) -> Generator[list[Fish], None, None]:
        """
        If negate is false return objects whose traits are subset of `traits`. Otherwise, return objects whose traits
        are disjoint with `traits`.
        """

        def filter_(object_: PondObject) -> bool:
            fish = cast(Fish, object_)
            return all(trait in traits for trait in fish.traits)

        for fish_layer in self.get_visible_objects_by_type(position, eyesight, [ObjectKind.FISH], False):
            new_list = []
            for fish in fish_layer:
                fish = cast("Fish", fish)
                if self._check_condition(fish, filter_, negate):
                    new_list.append(fish)
            if new_list:
                yield new_list

    def _get_visible_objects(
            self, position: Position, eyesight: int, object_filter: Callable[[PondObject], bool], negate: bool = False
    ) -> Generator[list[PondObject], None, None]:
        """Returns visible objects grouped by distance from `pos`. Groups are sorted in ascending order of distance"""

        for radius in range(eyesight):
            objects = self._get_objects_at_radius(radius, position, object_filter, negate)
            if objects:
                yield objects

    def _get_objects_at_radius(
            self, radius: int, position: Position, object_filter: Callable[[PondObject], bool], negate: bool = False
    ) -> list[PondObject]:
        offset = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        objects = []

        if radius == 0:
            return self._get_spot_objects(position, object_filter, negate)

        objects.extend(self._get_corner_objects(offset, radius, position, object_filter, negate))

        if radius == 1:
            return objects

        objects.extend(self._get_edge_objects(offset, radius, position, object_filter, negate))

        return objects

    def _get_spot_objects(
            self, position: Position, object_filter: Callable[[PondObject], bool], negate: bool
    ) -> list[PondObject]:
        objects = []
        for pond in self.ponds:
            for object_ in pond.get_spot(position):
                if self._check_condition(object_, object_filter, negate):
                    objects.append(object_)
        return objects

    def _get_corner_objects(
            self, offset: list[tuple[int, int]], radius: int, position: Position,
            object_filter: Callable[[PondObject], bool], negate: bool = False
    ) -> list[PondObject]:
        objects = []

        for (offset_x, offset_y) in offset:
            point = Position(position.y + offset_y * radius, position.x + offset_x * radius)
            if self._is_in_pond(point):
                objects.extend(self._get_spot_objects(point, object_filter, negate))

        return objects

    def _is_in_pond(self, position: Position) -> bool:
        return 0 <= position.x < self.pond_width and 0 <= position.y < self.pond_height

    def _get_edge_objects(
            self, offset: list[tuple[int, int]], radius: int, position: Position,
            object_filter: Callable[[PondObject], bool], negate: bool = False
    ) -> list[PondObject]:
        objects: list[PondObject] = []

        for point1, point2 in itertools.pairwise(offset + [(0, 1)]):
            self._get_edge_object(objects, point1, point2, position, radius, object_filter, negate)

        return objects

    def _get_edge_object(
            self, objects: list[PondObject], point1: tuple[int, int], point2: tuple[int, int], position: Position,
            radius: int, object_filter: Callable[[PondObject], bool], negate: bool
    ) -> None:
        x_change = point2[0] - point1[0]
        y_change = point2[1] - point1[1]
        p1 = Position(position.y + point1[1] * radius + y_change, position.x + point1[0] * radius + x_change)
        p2 = Position(position.y + point2[1] * radius - y_change, position.x + point2[0] * radius - x_change)

        (first_idx, last_idx) = self._get_visible_indices(p1, p2)

        if first_idx is None:
            return

        for i in range(first_idx, last_idx + 1):
            point = Position(p1.y + y_change * i, p1.x + x_change * i)
            objects.extend(self._get_spot_objects(point, object_filter, negate))

    def _get_visible_indices(self, point1: Position, point2: Position) -> tuple[Optional[int], Optional[int]]:
        x_indices, y_indices = self._get_all_visible_indices(point1, point2)
        if x_indices is None:
            return None, None

        self._ensure_indices_order(x_indices, y_indices)

        indices = self._get_intersection(x_indices[0], x_indices[1], y_indices[0], y_indices[1])
        if indices[0] > indices[1]:
            return None, None

        return indices

    def _get_all_visible_indices(
            self, point1: Position, point2: Position
    ) -> tuple[Optional[list[int]], Optional[list[int]]]:
        x_swapped = self._swap_x(point1, point2)
        y_swapped = self._swap_y(point1, point2)

        x_range = self._get_intersection(point1.x, point2.x, 0, self.pond_width - 1)
        y_range = self._get_intersection(point1.y, point2.y, 0, self.pond_height - 1)

        if x_range[0] > x_range[1] or y_range[0] > y_range[1]:
            return None, None

        self._restore_coordinates(point1, point2, x_swapped, y_swapped)

        x_indices = [abs(x_range[0] - point1.x), abs(x_range[1] - point1.x)]
        y_indices = [abs(y_range[0] - point1.y), abs(y_range[1] - point1.y)]

        return x_indices, y_indices

    @staticmethod
    def _swap_x(point1: Position, point2: Position) -> bool:
        if point1.x > point2.x:
            point1.x, point2.x = point2.x, point1.x
            return True
        return False

    @staticmethod
    def _swap_y(point1: Position, point2: Position) -> bool:
        if point1.y > point2.y:
            point1.y, point2.y = point2.y, point1.y
            return True
        return False

    @staticmethod
    def _restore_coordinates(point1: Position, point2: Position, x_swapped: bool, y_swapped: bool) -> None:
        if x_swapped:
            point1.x, point2.x = point2.x, point1.x
        if y_swapped:
            point1.y, point2.y = point2.y, point1.y

    @staticmethod
    def _ensure_indices_order(x_indices: list[int], y_indices: list[int]):
        if x_indices[0] > x_indices[1]:
            x_indices[0], x_indices[1] = x_indices[1], x_indices[0]
        if y_indices[0] > y_indices[1]:
            y_indices[0], y_indices[1] = y_indices[1], y_indices[0]

    @staticmethod
    def _get_intersection(a1, a2, b1, b2) -> tuple[int, int]:
        """Returns intersection of segment [a1, a2] with [b1, b2]"""
        return max(a1, b1), min(a2, b2)

    @staticmethod
    def _check_condition(object_: PondObject, object_filter: Callable[[PondObject], bool], negate: bool) -> bool:
        return object_filter(object_) if not negate else not object_filter(object_)

    def _get_x_coordinates(self, x: int, radius: int) -> tuple[int, int]:
        return max(0, x - radius + 1), min(self.pond_width - 1, x + radius - 1)

    def _get_y_coordinates(self, y: int, radius: int) -> tuple[int, int]:
        return max(0, y - radius + 1), min(self.pond_height - 1, y + radius - 1)

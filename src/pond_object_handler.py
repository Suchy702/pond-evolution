from typing import Iterable
from abc import ABC

from src.pond import Pond
from src.pond_object_database import PondObjectDatabase
from src.pond_object import PondObject


class PondObjectHandler(ABC):
    def __init__(self, pond_height: int, pond_width: int):
        self._pond: Pond = Pond(pond_height, pond_width)
        self._base: PondObjectDatabase = PondObjectDatabase()

    @property
    def amount(self):
        return self._base.size

    @property
    def all_objects(self):
        return self._base.objects

    def _add(self, obj: PondObject) -> None:
        self._base.add(obj)
        self._pond.add(obj)

    def _remove(self, obj: PondObject) -> None:
        self._base.remove(obj)
        self._pond.remove(obj)

    def add_many(self, objects: Iterable[PondObject]):
        for obj in objects:
            self._add(obj)

    def remove_many(self, objects: Iterable[PondObject]):
        for obj in objects:
            self._remove(obj)

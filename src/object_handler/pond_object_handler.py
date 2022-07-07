from typing import Iterable, Generator
from abc import ABC, abstractmethod

from src.pond import Pond
from src.pond_object_database import PondObjectDatabase
from src.object.pond_object import PondObject
from src.simulation_settings import SimulationSettings


class PondObjectHandler(ABC):
    def __init__(self, settings: SimulationSettings):
        self._pond: Pond = Pond(settings)
        self._object_database: PondObjectDatabase = PondObjectDatabase()

    @property
    def size(self) -> int:
        return self._object_database.size

    @property
    def objects(self) -> list[PondObject]:
        return self._object_database.objects

    def add(self, obj: PondObject) -> None:
        self._object_database.add(obj)
        self._pond.add(obj)

    def remove(self, obj: PondObject) -> None:
        self._object_database.remove(obj)
        self._pond.remove(obj)

    def add_all(self, objects: Iterable[PondObject]):
        for obj in objects:
            self.add(obj)

    def remove_all(self, objects: Iterable[PondObject]):
        for obj in objects:
            self.remove(obj)

    def update(self) -> None:
        for obj in self.objects:
            obj.update()

    def add_random(self, amount: int) -> None:
        self.add_all(self.create_random(amount))

    def create_random(self, amount: int) -> Generator[PondObject, None, None]:
        for i in range(amount):
            yield self.create_random_single()

    @abstractmethod
    def create_random_single(self) -> PondObject:
        pass

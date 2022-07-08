from functools import reduce
from typing import Iterable, Generator
from abc import ABC, abstractmethod

from overrides import overrides

from src.pond import Pond
from src.pond_object_database import PondObjectDatabase
from src.object.pond_object import PondObject
from src.position import Position
from src.simulation_settings import SimulationSettings


class PondObjectHandler(ABC):
    def __init__(self, settings: SimulationSettings):
        pass

    @abstractmethod
    def add_random(self, amount: int) -> None:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def objects(self) -> list[PondObject]:
        pass


class PondObjectHandlerHomogeneous(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self._pond: Pond = Pond(settings)
        self._object_database: PondObjectDatabase = PondObjectDatabase()

    @property
    @overrides
    def size(self) -> int:
        return self._object_database.size

    @property
    @overrides
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

    @overrides
    def add_random(self, amount: int) -> None:
        self.add_all(self.create_random(amount))

    def create_random(self, amount: int) -> Generator[PondObject, None, None]:
        for i in range(amount):
            yield self.create_random_single()

    @abstractmethod
    def create_random_single(self) -> PondObject:
        pass

    # Nie mozna ustawic zwracanego typu na set[PondObject] bo czasem zwracany jest Worm, czasem Fish i powstaje kolizja
    # gdy wiemy ze mamy fish i chcemy uzyc jej atrybutu, jednak Pycharm podpowiada nam ze PondObject nie ma takiego
    # atrybutu
    # TODO: możemy dać set[PondObject] i wtedy trzeba będzie castować na Fish/Worm czy cokolwiek. Tak samo jak robi się
    # to w Javie :( Jeżeli chcemy type hinty to musimy niestety odejsć troche od pythonowosci
    def get_spot_obj(self, pos: Position):
        return self._pond.get_spot(pos)

    def get_spot_energy_val(self, pos: Position) -> int:
        return sum([obj.energy_val for obj in self.get_spot_obj(pos)])

    # Wyrazenie listowe zeby zapobiec przekazaniu dalej referencji, co zmienialoby rozmiar setu podczas iteracji
    def remove_at_spot(self, pos: Position):
        self.remove_all([obj for obj in self._pond.get_spot(pos)])

    def is_sth_at_pos(self, pos) -> bool:
        return len(self._pond.get_spot(pos)) > 0


class PondObjectHandlerBundler(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self._handlers: list[PondObjectHandlerHomogeneous] = []

    @property
    @overrides
    def size(self) -> int:
        return reduce(lambda acc, h: acc + h.size, self._handlers, 0)

    @property
    @overrides
    def objects(self) -> list[PondObject]:
        return reduce(lambda list_, handler: list_ + handler.objects, self._handlers, [])

    @abstractmethod
    def add_random(self, amount: int) -> None:
        pass

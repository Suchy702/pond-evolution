from typing import Iterable
from abc import ABC

from src.pond import Pond
from src.pond_object_database import PondObjectDatabase
from src.pond_object import PondObject
from src.position import Position


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

    # Nie mozna ustawic zwracanego typu na set[PondObject] bo czasem zwracany jest Worm, czasem Fish i powstaje kolizja
    # gdy wiemy ze mamy fish i chcemy uzyc jej atrybutu, jednak Pycharm podpowiada nam ze PondObject nie ma takiego
    # atrybutu
    def get_spot_obj(self, pos: Position):
        return self._pond.get_spot(pos)

    def get_spot_energy_val(self, pos: Position) -> int:
        return sum([obj.energy_val for obj in self.get_spot_obj(pos)])

    # Wyrazenie listowe zeby zapobiec przekazaniu dalej referencji, co zmienialoby rozmiar setu podczas iteracji
    def remove_at_spot(self, pos: Position):
        self.remove_all([obj for obj in self._pond.get_spot(pos)])

    def _add(self, obj: PondObject) -> None:
        self._base.add(obj)
        self._pond.add(obj)

    def _remove(self, obj: PondObject) -> None:
        self._base.remove(obj)
        self._pond.remove(obj)

    def add_all(self, objects: Iterable[PondObject]) -> None:
        for obj in objects:
            self._add(obj)

    def remove_all(self, objects: Iterable[PondObject]) -> None:
        for obj in objects:
            self._remove(obj)

    def is_sth_at_pos(self, pos) -> bool:
        return len(self._pond.get_spot(pos)) > 0

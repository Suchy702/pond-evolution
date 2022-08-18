from abc import ABC, abstractmethod
from functools import reduce
from typing import Iterable, Generator

from overrides import overrides

from src.decision.decision_set import DecisionSet
from src.object.pond_object import PondObject
from src.pond.pond import Pond
from src.pond.pond_object_database import PondObjectDatabase
from src.pond.pond_viewer import PondViewer
from src.position import Position
from src.simulation_settings import SimulationSettings
from src.events.event_emitter import EventEmitter

event_emitter = EventEmitter()


class PondObjectHandler(ABC):
    def __init__(self, settings: SimulationSettings):
        self.settings: SimulationSettings = settings

    @abstractmethod
    def add_random(self, amount: int) -> None:
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @property
    @abstractmethod
    def objects(self) -> list[PondObject]:
        pass

    @abstractmethod
    def get_spot_objects(self, position: Position) -> set[PondObject]:
        pass

    @property
    @abstractmethod
    def ponds(self) -> list[Pond]:
        pass

    def get_decisions(self, pond_viewer: PondViewer) -> Generator[DecisionSet, None, None]:
        decisions = DecisionSet()
        for object_ in self.objects:
            decisions += object_.get_decisions(pond_viewer)

        yield decisions

    @abstractmethod
    def handle_decisions(self, decisions: DecisionSet):
        pass


class PondObjectHandlerHomogeneous(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self._pond: Pond = Pond(settings)
        self._object_database: PondObjectDatabase = PondObjectDatabase()
        self.event_emitter: EventEmitter = event_emitter

    @property  # type: ignore
    @overrides
    def size(self) -> int:
        return self._object_database.size

    @property  # type: ignore
    @overrides
    def objects(self) -> list[PondObject]:
        return self._object_database.objects

    @property  # type: ignore
    @overrides
    def ponds(self) -> list[Pond]:
        return [self._pond]

    def add(self, object_: PondObject) -> None:
        self._object_database.add(object_)
        self._pond.add(object_)

    def remove(self, object_: PondObject) -> None:
        self._object_database.remove(object_)
        self._pond.remove(object_)

    def add_all(self, objects: Iterable[PondObject]) -> None:
        for object_ in objects:
            self.add(object_)

    def remove_all(self, objects: Iterable[PondObject]) -> None:
        for object_ in objects:
            self.remove(object_)

    @overrides
    def add_random(self, amount: int) -> None:
        self.add_all(self.create_random(amount))

    def create_random(self, amount: int) -> Generator[PondObject, None, None]:
        for _ in range(amount):
            yield self.create_random_single()

    @abstractmethod
    def create_random_single(self) -> PondObject:
        pass

    @overrides
    def get_spot_objects(self, position: Position) -> set[PondObject]:
        return self._pond.get_spot(position)

    def get_spot_energy_value(self, pos: Position) -> int:
        return sum([obj.energy_value for obj in self.get_spot_objects(pos)])

    def remove_at_spot(self, pos: Position) -> None:
        self.remove_all(list(self._pond.get_spot(pos)))

    def is_position_nonempty(self, pos) -> bool:
        return len(self._pond.get_spot(pos)) > 0


class PondObjectHandlerBundler(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self._handlers: list[PondObjectHandlerHomogeneous] = []

    @property  # type: ignore
    @overrides
    def size(self) -> int:
        return reduce(lambda acc, h: acc + h.size, self._handlers, 0)

    @property  # type: ignore
    @overrides
    def objects(self) -> list[PondObject]:
        return reduce(lambda list_, handler: list_ + handler.objects, self._handlers, [])

    @property  # type: ignore
    @overrides
    def ponds(self) -> list[Pond]:
        return reduce(lambda list_, handler: list_ + handler.ponds, self._handlers, [])

    @abstractmethod
    def add_random(self, amount: int) -> None:
        pass

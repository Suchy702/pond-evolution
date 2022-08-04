from src.events.event import LogicEvent
from src.logic.interactor import Interactor
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandler
from src.simulation_settings import SimulationSettings


class Engine:
    def __init__(self, settings: SimulationSettings):
        self._settings: SimulationSettings = settings
        self._interactor: Interactor = Interactor(self._settings)
        self._cycle_count: int = 0

    def demo(self) -> None:
        self._interactor.preparations()

    @property
    def all_objects(self) -> list[PondObject]:
        return self._interactor.all_objects

    @property
    def all_handlers(self) -> list[PondObjectHandler]:
        return self._interactor.handlers

    def show_pond(self) -> None:
        board: list[list[list[str]]] = [
            [[] for _ in range(self._settings.pond_width)] for _ in range(self._settings.pond_height)
        ]
        for obj in self.all_objects:
            board[obj.pos.y][obj.pos.x].append(str(obj))
        for row in board:
            print(row)

    def cycle(self) -> None:
        # Order is important
        self._interactor.remove_unnecessary_objects()
        self._interactor.handle_decisions()
        self._interactor.feed_fish()
        self._cycle_count += 1

    def add_obj_by_click(self, event: LogicEvent) -> None:
        self._interactor.add_obj_by_click(event)
from src.simulation_settings import SimulationSettings
from src.interactor import Interactor


class Engine:
    def __init__(self, settings: SimulationSettings):
        self._settings: SimulationSettings = settings
        self._interactor: Interactor = Interactor(self._settings)

    @property
    def all_objects(self):
        return self._interactor.all_objects

    def show_pond(self) -> None:
        board: list[list[list[str]]] = [
            [[] for _ in range(self._settings.pond_width)] for _ in range(self._settings.pond_height)
        ]
        for obj in self.all_objects:
            board[obj.pos.y][obj.pos.x].append(str(obj))
        for row in board:
            print(row)

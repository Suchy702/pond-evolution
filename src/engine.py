from src.interactor import Interactor
from src.simulation_settings import SimulationSettings


class Engine:
    def __init__(self, settings: SimulationSettings):
        self._settings: SimulationSettings = settings
        self._interactor: Interactor = Interactor(self._settings)
        self._cycle_count: int = 0

    def demo(self):
        self._interactor.preparations()

    @property
    def all_objects(self):
        return self._interactor.all_objects

    @property
    def all_handlers(self):
        return self._interactor.handlers

    def show_pond(self) -> None:
        board: list[list[list[str]]] = [
            [[] for _ in range(self._settings.pond_width)] for _ in range(self._settings.pond_height)
        ]
        for obj in self.all_objects:
            board[obj.pos.y][obj.pos.x].append(str(obj))
        for row in board:
            print(row)

    # Kolejnosc:
    # Usuwanie niepotrzebnych elementow
    # Poruszanie sie
    # Jedzenie
    # Pojawianie sie nowych obiektow
    def cycle(self):
        self._interactor.remove_unnecessary_objects()
        self._interactor.handle_decisions()
        self._interactor.move_objects()
        self._interactor.feed_fish()
        self._interactor.add_new_objects(self._cycle_count)
        self._cycle_count += 1

from src.simulation_settings import SimulationSettings
from src.interactor import Interactor


class Engine:
    def __init__(self, settings: SimulationSettings):
        self._settings: SimulationSettings = settings
        self._interactor: Interactor = Interactor(self._settings)
        self._cycle_count: int = 0

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

    # Kolejnosc:
    # Usuwanie niepotrzebnych elementow
    # Poruszanie sie
    # Jedzenie
    # Pojawianie sie nowych obiektow
    def cycle(self):
        self._interactor.remove_unnecessary_objects()
        self._interactor.move_objects()
        self._interactor.feed_fishes()
        self._interactor.put_new_objects()

    # Symulacja dla testow, normalnie powinno byc  w Game
    def symulation(self):
        self._interactor.preparations()
        while True:
            self.show_pond()
            self.cycle()
            next_cycle_stop = input()
            self._cycle_count += 1


if __name__ == "__main__":
    engine = Engine(SimulationSettings(10, 5))
    engine.symulation()

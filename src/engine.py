from functools import reduce

from src.object_handler.worm_handler import WormHandler
from src.object_handler.plant_handler import PlantHandler
from src.object_handler.fish_handler import FishHandler
from src.simulation_settings import SimulationSettings


class Engine:
    def __init__(self, settings: SimulationSettings):
        self.settings = settings

        self._fish_handler: FishHandler = FishHandler(settings)
        self._worm_handler: WormHandler = WormHandler(settings)
        self._plant_handler: PlantHandler = PlantHandler(settings)
        self._handlers = [self._fish_handler, self._worm_handler, self._plant_handler]

    @property
    def all_objects(self):
        return reduce(lambda list_, handler: list_ + handler.objects, self._handlers, [])

    # beta function for testing
    def preparations(self):
        for handler in self._handlers:
            handler.add_random(5)

    def show_pond(self):
        board: list[list[list[str]]] = [
            [[] for _ in range(self.settings.pond_width)] for _ in range(self.settings.pond_height)
        ]
        for obj in self.all_objects:
            board[obj.pos.y][obj.pos.x].append(str(obj))
        for row in board:
            print(row)

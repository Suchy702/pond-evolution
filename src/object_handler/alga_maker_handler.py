from overrides import overrides

from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandler
from src.position import Position
from src.simulation_settings import SimulationSettings

# TODO ta klasa troche nic nie robi. Może ją zmergować z PlantHandler?
class AlgaMakerHandler(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = self._pond.height - 1
        return AlgaMaker(pos)

from overrides import overrides

from src.constants import ALGA_ENERGY_VALUE
from src.object.alga import Alga
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandler
from src.position import Position
from src.simulation_settings import SimulationSettings


class AlgaHandler(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        return Alga(ALGA_ENERGY_VALUE, pos, self._pond.height)

    # TODO: move to update() or new class or make private
    def move_algae(self) -> None:
        for algae in self.objects:
            self._pond.change_position(algae, self._pond.trim_position(algae))

    # TODO: move to update() or new class or make private
    def kill_algae_on_surface(self) -> None:
        to_del = []
        for alg in self.objects:
            if self._pond.is_on_surface(alg.pos):
                to_del.append(alg)
        self.remove_all(to_del)

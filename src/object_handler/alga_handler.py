from typing import cast

from overrides import overrides

from src.constants import ALGA_ENERGY_VALUE
from src.object.alga import Alga
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings


class AlgaHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def algae(self):
        return [cast(Alga, alga) for alga in self.objects]

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        return Alga(ALGA_ENERGY_VALUE, pos, self._pond.height)

    def move_algae(self) -> None:
        for algae in self.algae:
            self._pond.change_position(algae, self._pond.trim_position(algae.find_pos_to_move()))

    def kill_algae_on_surface(self) -> None:
        self.remove_all([alga for alga in self.algae if self._pond.is_on_surface(alga.pos)])

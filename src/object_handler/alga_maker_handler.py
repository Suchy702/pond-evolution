from typing import cast

from overrides import overrides

from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings


class AlgaMakerHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = self._pond.height - 1
        return AlgaMaker(pos, self._pond.height)

    def create_algae(self) -> list[Alga]:
        algae = []
        for algae_maker in self.objects:
            algae_maker = cast(AlgaMaker, algae_maker)
            algae.extend(algae_maker.create_algae())
        return algae

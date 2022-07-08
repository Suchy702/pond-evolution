from typing import cast

from overrides import overrides

from itertools import chain

from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings


class AlgaMakerHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def alga_makers(self):
        return [cast(AlgaMaker, alga_maker) for alga_maker in self.objects]

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = self._pond.height - 1
        return AlgaMaker(pos, self._pond.height)

    def create_algae(self) -> list[Alga]:
        return list(chain.from_iterable([alga_maker.create_algae(self._pond) for alga_maker in self.alga_makers]))


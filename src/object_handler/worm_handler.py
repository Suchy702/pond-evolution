from typing import cast

from overrides import overrides

from src.constants import WORM_ENERGY_VALUE
from src.object.pond_object import PondObject
from src.object.worm import Worm
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings


class WormHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = 0
        return Worm(WORM_ENERGY_VALUE, pos, self._pond.shape)

    def move_worms(self) -> None:
        for worm in self.objects:
            worm = cast(Worm, worm)
            self._pond.change_position(worm, self._pond.trim_position(worm.find_pos_to_move()))

    def kill_worms_on_ground(self) -> None:
        to_del = []
        for worm in self.objects:
            if self._pond.is_on_ground(worm.pos):
                to_del.append(worm)
        self.remove_all(to_del)

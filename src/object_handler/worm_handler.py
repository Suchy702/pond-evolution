from typing import cast

from overrides import overrides

from src.constants import WORM_ENERGY_VALUE, NUM_OF_NEW_WORMS_AT_CYCLE
from src.object.pond_object import PondObject
from src.object.worm import Worm
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings


class WormHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def worms(self):
        return [cast(Worm, worm) for worm in self.objects]

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = 0
        return Worm(WORM_ENERGY_VALUE, pos, self._pond.shape)

    def put_new_worms(self) -> None:
        self.add_all([self.create_random_single() for _ in range(NUM_OF_NEW_WORMS_AT_CYCLE)])

    def move_worms(self) -> None:
        for worm in self.worms:
            self._pond.change_position(worm, self._pond.trim_position(worm.find_pos_to_move()))

    def remove_worms_on_the_ground(self) -> None:
        self.remove_all([worm for worm in self.worms if self._pond.is_on_ground(worm.pos)])

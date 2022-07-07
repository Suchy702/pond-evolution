from overrides import overrides

from src.constants import WORM_ENERGY_VALUE
from src.object.pond_object import PondObject
from src.object.worm import Worm
from src.object_handler.pond_object_handler import PondObjectHandler
from src.simulation_settings import SimulationSettings


class WormHandler(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @overrides
    def create_random_single(self) -> PondObject:
        pos = self._pond.random_position()
        pos.y = 0
        return Worm(WORM_ENERGY_VALUE, pos, self._pond.shape)

    # TODO: type hintsy pond object nie ma find_pos_to_move
    def move_worms(self) -> None:
        for worm in self.objects:
            self._pond.change_position(worm, self._pond.trim_position(worm.find_pos_to_move()))

    def del_worms_from_ground(self) -> None:
        to_del = []
        for worm in self.objects:
            if self._pond.is_on_ground(worm.pos):
                to_del.append(worm)
        self.remove_all(to_del)

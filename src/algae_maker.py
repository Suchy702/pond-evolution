from random import randint

from src.pond_object import PondObject
from src.position import Position

ALGAE_ENERGY_VAL = 15
MAX_ALGS_CREATING = 3
MIN_ALGS_CREATING = 1


class AlgaeMaker(PondObject):
    def __init__(self, pos: Position):
        super().__init__('M', pos)
        self.min_algs_create: int = MIN_ALGS_CREATING
        self.max_algs_create: int = MAX_ALGS_CREATING

    @property
    def created_algs_amonut(self):
        return randint(self.min_algs_create, self.max_algs_create)

    def _find_pos_to_create_alg(self) -> Position:
        return self.pos.changed(1, randint(-1, 1))

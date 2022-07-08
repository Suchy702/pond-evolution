from random import randint

from src.constants import MAX_ALGAE_TO_CREATE, MIN_ALGAE_TO_CREATE, ALGA_ENERGY_VALUE
from src.object.alga import Alga
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class AlgaMaker(PondObject):
    def __init__(self, pos: Position, pond_height: int):
        super().__init__(ObjectKind.ALGA_MAKER, pos)
        self.min_algae_to_create: int = MIN_ALGAE_TO_CREATE
        self.max_algae_to_create: int = MAX_ALGAE_TO_CREATE
        self._pond_height: int = pond_height

    def create_alga(self) -> Alga:
        return Alga(ALGA_ENERGY_VALUE, self._find_pos_to_create_alg(), self._pond_height)

    def choose_algae_amount(self) -> int:
        return int(randint(self.min_algae_to_create, self.max_algae_to_create))

    def create_algae(self) -> list[Alga]:
        return [self.create_alga() for _ in range(self.choose_algae_amount())]

    def _find_pos_to_create_alg(self) -> Position:
        return self.pos.changed(1, randint(-1, 1))

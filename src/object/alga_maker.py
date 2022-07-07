from random import randint

from overrides import overrides

from src.constants import MAX_ALGAE_TO_CREATE, MIN_ALGAE_TO_CREATE
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class AlgaMaker(PondObject):
    def __init__(self, pos: Position):
        super().__init__(ObjectKind.MAKER, pos)
        self.min_algae_to_create: int = MIN_ALGAE_TO_CREATE
        self.max_algae_to_create: int = MAX_ALGAE_TO_CREATE

    def choose_algae_amount(self) -> int:
        return randint(self.min_algae_to_create, self.max_algae_to_create)

    # TODO: move to update() or new class
    def _find_pos_to_create_alg(self) -> Position:
        return self.pos.changed(1, randint(-1, 1))

    @overrides
    def update(self) -> None:
        pass

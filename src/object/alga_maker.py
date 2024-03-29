from random import randint

from src.ai.alga_maker_ai import AlgaMakerAI
from src.constants import ALGA_DEFAULT_ENERGY_VALUE
from src.object.alga import Alga
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.pond.pond import Pond
from src.position import Position


class AlgaMaker(PondObject):
    def __init__(self, position: Position, pond_height: int):
        super().__init__(ObjectKind.ALGA_MAKER, position, AlgaMakerAI(self))
        self._pond_height: int = pond_height

    def create_algae(self, pond: Pond, intensity: int) -> list[Alga]:
        return [self.create_alga(pond) for _ in range(self.choose_algae_amount(intensity))]

    def create_alga(self, pond: Pond) -> Alga:
        return Alga(ALGA_DEFAULT_ENERGY_VALUE, pond.trim_position(self._find_pos_to_create_alg()), self._pond_height)

    @staticmethod
    def choose_algae_amount(intensity: int) -> int:
        return int(randint(intensity, int(intensity*1.5)))

    def _find_pos_to_create_alg(self) -> Position:
        return self.position.changed(1, randint(-1, 1))

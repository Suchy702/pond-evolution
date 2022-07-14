from src.ai.ai import AlgaAI
from src.constants import ALGA_SURFACING_STEPS
from src.object.pond_object import PondObject
from src.object_kind import ObjectKind
from src.position import Position


class Alga(PondObject):
    def __init__(self, energy_val: int, pos: Position, pond_height: int):
        super().__init__(ObjectKind.ALGA, pos, AlgaAI(self))
        self._energy_val: int = energy_val
        self.surfacing_speed: int = max(1, pond_height // ALGA_SURFACING_STEPS)

    @property
    def energy_val(self) -> int:
        return self._energy_val

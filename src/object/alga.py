from src.ai.alga_ai import AlgaAI
from src.constants import ALGA_SURFACING_STEPS
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.position import Position


class Alga(PondObject):
    def __init__(self, energy_value: int, position: Position, pond_height: int):
        super().__init__(ObjectKind.ALGA, position, AlgaAI(self))
        self._energy_value = energy_value
        self.surfacing_speed: int = max(1, pond_height // ALGA_SURFACING_STEPS)

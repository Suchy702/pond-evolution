from src.ai.worm_ai import WormAI
from src.constants import WORM_FALLING_STEPS, WORM_BOUNCE_STEPS
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.position import Position


class Worm(PondObject):
    def __init__(self, energy_val: int, pos: Position, pond_shape: tuple[int, int]):
        super().__init__(ObjectKind.WORM, pos, WormAI(self))
        self._energy_val: int = energy_val
        self.falling_speed: int = max(1, pond_shape[0] // WORM_FALLING_STEPS)
        self.bounce_ratio: int = max(1, pond_shape[1] // WORM_BOUNCE_STEPS)

    @property
    def energy_val(self) -> int:
        return self._energy_val

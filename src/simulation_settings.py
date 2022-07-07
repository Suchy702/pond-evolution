from dataclasses import dataclass

from src.constants import POND_WIDTH, POND_HEIGHT


@dataclass
class SimulationSettings:
    pond_width: int = POND_WIDTH
    pond_height: int = POND_HEIGHT

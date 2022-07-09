from dataclasses import dataclass

from src.constants import POND_WIDTH, POND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, LOGIC_DELAY


@dataclass
class SimulationSettings:
    pond_width: int = POND_WIDTH
    pond_height: int = POND_HEIGHT

    screen_width: int = SCREEN_WIDTH
    screen_height: int = SCREEN_HEIGHT

    logic_delay: int = LOGIC_DELAY

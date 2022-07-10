from dataclasses import dataclass

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, ANIMATION_SPEED, CELL_MIN_PX_SIZE


@dataclass
class SimulationSettings:
    screen_width: int = SCREEN_WIDTH
    screen_height: int = SCREEN_HEIGHT

    pond_width: int = SCREEN_WIDTH // CELL_MIN_PX_SIZE
    pond_height: int = SCREEN_HEIGHT // CELL_MIN_PX_SIZE

    animation_speed: int = ANIMATION_SPEED


from src.simulation_settings import SimulationSettings

from src.constants import CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE, START_ANIMATION_FPS, MAX_ANIMATION_FPS, MIN_ANIMATION_FPS


def clip(val: int, a: int, b: int) -> int:
    # Clips `val` to range [min(a, b), max(a, b)]
    if a > b:
        a, b = b, a
    return min(max(val, a), b)


class GraphicValuesGuard:
    def __init__(self, settings: SimulationSettings):
        self._settings = settings
        self._cell_size: int = CELL_MIN_PX_SIZE  # length of cell's side in px. Cell is a square
        self._animation_speed: int = START_ANIMATION_FPS
        self._x_offset: int = 0
        self._y_offset: int = 0

    @property
    def x_offset(self) -> int:
        return self._x_offset

    @x_offset.setter
    def x_offset(self, val: int) -> None:
        x_offset_limit = -(self._settings.pond_width * self._cell_size - self._settings.screen_pond_width)
        self._x_offset = clip(val, 0, x_offset_limit)

    @property
    def y_offset(self) -> int:
        return self._y_offset

    @y_offset.setter
    def y_offset(self, val: int) -> None:
        y_offset_limit = -(self._settings.pond_height * self._cell_size - self._settings.screen_pond_height)
        self._y_offset = clip(val, 0, y_offset_limit)

    @property
    def cell_size(self) -> int:
        return self._cell_size

    @cell_size.setter
    def cell_size(self, val: int) -> None:
        self._cell_size = clip(val, CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE)

    @property
    def animation_speed(self) -> int:
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, val: int) -> None:
        self._animation_speed = clip(val, MIN_ANIMATION_FPS, MAX_ANIMATION_FPS)
import math
from math import ceil
from typing import Optional

from numba import jit
from src.constants import FISH_MAX_SIZE, FISH_MIN_SIZE, CELL_MAX_PX_SIZE, CELL_MIN_PX_SIZE


class JITGraphicCalculator:
    @staticmethod
    @jit(nopython=True)
    def is_not_linear_fun(x1: int, x2: int) -> bool:
        return x1 == x2

    @staticmethod
    @jit(nopython=True)
    def get_position_for_non_linear_function(x1: int, y1: int, y2: int, step: int, total_steps: int) -> tuple[int, int]:
        dist = y2 - y1
        y = y1 + dist * step / total_steps
        x = x1
        return int(x), int(y)

    @staticmethod
    @jit(nopython=True)
    def get_position_for_linear_function(x1: int, y1: int, x2: int, y2: int, step: int, total_steps: int) -> tuple[int, int]:
        dist = x2 - x1
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

        x = x1 + dist * step / total_steps
        y = a * x + b
        return int(x), int(y)

    @staticmethod
    @jit(nopython=True)
    def get_fish_size(fish_size: int, cell_size: int) -> int:
        percentage = (fish_size - FISH_MIN_SIZE) / (FISH_MAX_SIZE - FISH_MIN_SIZE)
        scale = 1 + percentage - 0.5

        return int(cell_size * scale)

    @staticmethod
    @jit(nopython=True)
    def center_position(x: int, y: int, cell_size: int, size: int) -> tuple[int, int]:
        x += (cell_size - size) // 2
        y += (cell_size - size) // 2
        return x, y

    @staticmethod
    @jit(nopython=True)
    def get_stay_animation_position(e_x: int, e_y: int, cell_size: int, x_off: int, y_off: int) -> tuple[int, int]:
        x = e_x * cell_size + x_off
        y = e_y * cell_size + y_off
        return x, y

    @staticmethod
    @jit(nopython=True)
    def get_start_point_of_animation(x: int, y: int, cell_size: int, x_off: int, y_off: int) -> tuple[int, int]:
        x = x * cell_size + x_off
        y = y * cell_size + y_off
        return x, y

    @staticmethod
    @jit(nopython=True)
    def get_end_point_of_animation(x: int, y: int, cell_size: int, x_off: int, y_off: int) -> tuple[int, int]:
        x = x * cell_size + x_off
        y = y * cell_size + y_off
        return x, y

    @staticmethod
    @jit(nopython=True)
    def get_visible_x_coordinates(x_off: int, cell_size: int, screen_pond_width: int) -> tuple[int, int]:
        x_min = int(ceil(-x_off / cell_size))
        x_max = (screen_pond_width - cell_size - x_off) // cell_size
        return x_min, x_max

    @staticmethod
    @jit(nopython=True)
    def get_visible_y_coordinates(y_off: int, cell_size: int, screen_pond_height: int) -> tuple[int, int]:
        y_min = int(ceil(-y_off / cell_size))
        y_max = (screen_pond_height - cell_size - y_off) // cell_size
        return y_min, y_max

    @staticmethod
    @jit(nopython=True)
    def get_rotation_angle(x: int, y: int) -> Optional[float]:
        if x == 0 and y == 0:
            return None

        degree = math.atan2(y, x) * 180 / math.pi

        if -90 <= degree <= 90:
            return degree
        elif 90 < degree < 180:
            return degree - 180
        return degree + 180

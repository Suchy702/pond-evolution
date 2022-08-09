from numba import jit
from src.constants import FISH_MAX_SIZE, FISH_MIN_SIZE, CELL_MAX_PX_SIZE, CELL_MIN_PX_SIZE

class JITGraphicCalculator:
    def __init__(self):
        pass

    @staticmethod
    @jit(nopython=True)
    def is_not_linear_fun(x1: int, x2: int) -> bool:
        return x1 == x2

    @staticmethod
    @jit(nopython=True)
    def calc_pos_for_non_linear_fun(x1: int, y1: int, y2: int, step: int, total_steps: int) -> tuple[int, int]:
        dist = y2 - y1
        y = y1 + dist * step / total_steps
        x = x1
        return int(x), int(y)

    @staticmethod
    @jit(nopython=True)
    def calc_pos_for_linear_fun(x1: int, y1: int, x2: int, y2: int, step: int, total_steps: int) -> tuple[int, int]:
        dist = x2 - x1
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

        x = x1 + dist * step / total_steps
        y = a * x + b
        return int(x), int(y)

    @staticmethod
    @jit(nopython=True)
    def match_size_for_fish_calculations(fish_size: int, cell_size: int) -> int:
        size = int(fish_size / ((FISH_MAX_SIZE + FISH_MIN_SIZE) // 2) * cell_size)
        return min(max(size, CELL_MIN_PX_SIZE), CELL_MAX_PX_SIZE)

    @staticmethod
    @jit(nopython=True)
    def reform_pos_to_be_in_center_of_cell(x: int, y: int, cell_size: int, size: int) -> tuple[int, int]:
        x += (cell_size - size) // 2
        y += (cell_size - size) // 2
        return x, y
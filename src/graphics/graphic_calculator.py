from math import ceil, copysign

from numba import jit

from src.events.event import GraphicEvent
from src.events.event_type import GraphicEventType
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.simulation_settings import SimulationSettings


class GraphicCalculator:
    def __init__(self, settings: SimulationSettings):
        self.settings = settings

    def get_visible_gird_x_coordinates(self, vals: GraphicValuesGuard) -> tuple[int, int]:
        x_min = int(ceil(-vals.x_offset / vals.cell_size))
        x_max = (self.settings.screen_pond_width - vals.cell_size - vals.x_offset) // vals.cell_size
        return x_min, x_max

    def get_visible_grid_y_coordinates(self, vals: GraphicValuesGuard) -> tuple[int, int]:
        y_min = int(ceil(-vals.y_offset / vals.cell_size))
        y_max = (self.settings.screen_pond_height - vals.cell_size - vals.y_offset) // vals.cell_size
        return y_min, y_max

    def get_visible_grid_coordinates(self, vals) -> tuple[int, int, int, int]:
        x_min, x_max = self.get_visible_gird_x_coordinates(vals)
        y_min, y_max = self.get_visible_grid_y_coordinates(vals)
        return x_min, x_max, y_min, y_max

    def calc_center_view(self, vals: GraphicValuesGuard) -> tuple[int, int]:
        new_x_offset = int(self.settings.screen_pond_width / 2 - self.settings.pond_width * vals.cell_size / 2)
        new_y_offset = int(self.settings.screen_pond_height / 2 - self.settings.pond_height * vals.cell_size / 2)
        return new_x_offset, new_y_offset

    @staticmethod
    @jit(nopython=True)
    def _is_not_linear_fun(x1: int, x2: int) -> bool:
        return x1 == x2

    @staticmethod
    @jit(nopython=True)
    def _calc_pos_for_non_linear_fun(x1: int, y1: int, y2: int, step: int, total_steps: int) -> tuple[int, int]:
        dist = y2 - y1
        y = y1 + dist * step / total_steps
        x = x1
        return int(x), int(y)

    @staticmethod
    @jit(nopython=True)
    def _calc_pos_for_linear_fun(x1: int, y1: int, x2: int, y2: int, step: int, total_steps: int) -> tuple[int, int]:
        dist = x2 - x1
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

        x = x1 + dist * step / total_steps
        y = a * x + b
        return int(x), int(y)

    @staticmethod
    def _calc_begin_point_in_animation(event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        x = event.from_x * vals.cell_size + vals.x_offset
        y = event.from_y * vals.cell_size + vals.y_offset
        return x, y

    @staticmethod
    def _calc_end_point_in_animation(event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        x = event.to_x * vals.cell_size + vals.x_offset
        y = event.to_y * vals.cell_size + vals.y_offset
        return x, y

    def _find_pos_to_draw_when_move(self, event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        x1, y1 = self._calc_begin_point_in_animation(event, vals)
        x2, y2 = self._calc_end_point_in_animation(event, vals)

        if self._is_not_linear_fun(x1, x2):
            return self._calc_pos_for_non_linear_fun(x1, y1, y2, event.step, event.total_steps)
        else:
            return self._calc_pos_for_linear_fun(x1, y1, x2, y2, event.step, event.total_steps)

    @staticmethod
    def _find_pos_to_draw_when_stay(event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        x = event.x * vals.cell_size + vals.x_offset
        y = event.y * vals.cell_size + vals.y_offset
        return x, y

    def find_pos_to_draw(self, event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        if event.event_type == GraphicEventType.ANIM_MOVE:
            return self._find_pos_to_draw_when_move(event, vals)
        else:
            return self._find_pos_to_draw_when_stay(event, vals)

    def get_click_coor(self, click_pos: tuple[int, int], vals: GraphicValuesGuard) -> tuple[int, int]:
        x_min, x_max, y_min, y_max = self.get_visible_grid_coordinates(vals)
        x, y = click_pos

        x_cell_add = x // vals.cell_size
        y_cell_add = y // vals.cell_size

        return x_min + x_cell_add, y_min + y_cell_add

    # Magic function
    def calc_zoom(self, change: int, vals: GraphicValuesGuard) -> None:
        old_cell_size = vals.cell_size
        vals.cell_size += change

        if vals.cell_size == old_cell_size:
            return

        """
        The idea is to find distance between point in the middle of the screen and point in the middle ozond and
        then inspect how this distance changes upon cell_size change
        """

        pond_center_x: float = vals.x_offset + old_cell_size * self.settings.pond_width // 2
        pond_center_y: float = vals.y_offset + old_cell_size * self.settings.pond_height // 2

        if self.settings.pond_width % 2 == 1:
            pond_center_x += old_cell_size / 2

        if self.settings.pond_height % 2 == 1:
            pond_center_y += old_cell_size / 2

        screen_center_x = self.settings.screen_pond_width / 2
        screen_center_y = self.settings.screen_pond_height / 2

        vertical_cells = min(
            abs(screen_center_x - pond_center_x) / old_cell_size,
            self.settings.pond_width / 2
        ) * copysign(1, screen_center_x - pond_center_x)
        horizontal_cells = min(
            abs(screen_center_y - pond_center_y) / old_cell_size,
            self.settings.screen_pond_height / 2
        ) * copysign(1, screen_center_y - pond_center_y)

        diff_x = screen_center_x - pond_center_x
        diff_y = screen_center_y - pond_center_y

        diff_x_after_zoom = diff_x + vertical_cells * change
        diff_y_after_zoom = diff_y + horizontal_cells * change

        # pond center after zoom
        pond_center_x = vals.x_offset + vals.cell_size * self.settings.pond_width // 2
        pond_center_y = vals.y_offset + vals.cell_size * self.settings.pond_height // 2

        # point to which current screen center is transformed after zoom
        old_screen_center_x = pond_center_x + diff_x_after_zoom
        old_screen_center_y = pond_center_y + diff_y_after_zoom

        vals.x_offset += int(screen_center_x - old_screen_center_x)
        vals.y_offset += int(screen_center_y - old_screen_center_y)
from math import copysign
from typing import cast

from src.events.event import GraphicEvent
from src.events.event_type import GraphicEventType
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.object.fish import Fish
from src.simulation_settings import SimulationSettings
from src.graphics.jit_graphic_calculator import JITGraphicCalculator


class GraphicCalculator:
    def __init__(self, settings: SimulationSettings):
        self._settings: SimulationSettings = settings
        self.jit_calc: JITGraphicCalculator = JITGraphicCalculator()

    def get_visible_grid_coordinates(self, vals) -> tuple[int, int, int, int]:
        cell_size, x_off, y_off = vals.cell_size, vals.x_offset, vals.y_offset
        x_min, x_max = self.jit_calc.get_visible_gird_x_coor(x_off, cell_size, self._settings.screen_pond_width)
        y_min, y_max = self.jit_calc.get_visible_grid_y_coor(y_off, cell_size, self._settings.screen_pond_height)
        return x_min, x_max, y_min, y_max

    def calc_center_view(self, vals: GraphicValuesGuard) -> tuple[int, int]:
        new_x_offset = int(self._settings.screen_pond_width / 2 - self._settings.pond_width * vals.cell_size / 2)
        new_y_offset = int(self._settings.screen_pond_height / 2 - self._settings.pond_height * vals.cell_size / 2)
        return new_x_offset, new_y_offset

    def match_size_for_fish(self, event: GraphicEvent, vals: GraphicValuesGuard) -> int:
        fish = cast(Fish, event.pond_object)
        return self.jit_calc.match_size_for_fish_calculations(fish.size, vals.cell_size)

    def _find_pos_to_draw_when_move(self, event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        cell_size, x_off, y_off = vals.cell_size, vals.x_offset, vals.y_offset
        x1, y1 = self.jit_calc.calc_begin_point_of_animation(event.from_x, event.from_y, cell_size, x_off, y_off)
        x2, y2 = self.jit_calc.calc_end_point_of_animation(event.to_x, event.to_y, cell_size, x_off, y_off)

        if self.jit_calc.is_not_linear_fun(x1, x2):
            return self.jit_calc.calc_pos_for_non_linear_fun(x1, y1, y2, event.step, event.total_steps)

        return self.jit_calc.calc_pos_for_linear_fun(x1, y1, x2, y2, event.step, event.total_steps)

    def reform_pos_to_be_in_center(self, x: int, y: int, vals: GraphicValuesGuard, size: int) -> tuple[int, int]:
        return self.jit_calc.reform_pos_to_be_in_center_of_cell(x, y, vals.cell_size, size)

    def find_pos_to_draw(self, event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        if event.event_type == GraphicEventType.ANIM_MOVE:
            return self._find_pos_to_draw_when_move(event, vals)
        else:
            return self.jit_calc.find_pos_to_draw_stay(event.x, event.y, vals.cell_size, vals.x_offset, vals.y_offset)

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
        The idea is to find distance between point in the middle of the screen and point in the middle of the pond, and
        then inspect how this distance changes upon cell_size change.
        """

        pond_center_x: float = vals.x_offset + old_cell_size * self._settings.pond_width // 2
        pond_center_y: float = vals.y_offset + old_cell_size * self._settings.pond_height // 2

        if self._settings.pond_width % 2 == 1:
            pond_center_x += old_cell_size / 2

        if self._settings.pond_height % 2 == 1:
            pond_center_y += old_cell_size / 2

        screen_center_x = self._settings.screen_pond_width / 2
        screen_center_y = self._settings.screen_pond_height / 2

        vertical_cells = min(
            abs(screen_center_x - pond_center_x) / old_cell_size,
            self._settings.pond_width / 2
        ) * copysign(1, screen_center_x - pond_center_x)

        horizontal_cells = min(
            abs(screen_center_y - pond_center_y) / old_cell_size,
            self._settings.screen_pond_height / 2
        ) * copysign(1, screen_center_y - pond_center_y)

        diff_x = screen_center_x - pond_center_x
        diff_y = screen_center_y - pond_center_y

        diff_x_after_zoom = diff_x + vertical_cells * change
        diff_y_after_zoom = diff_y + horizontal_cells * change

        # pond center after zoom
        pond_center_x = vals.x_offset + vals.cell_size * self._settings.pond_width // 2
        pond_center_y = vals.y_offset + vals.cell_size * self._settings.pond_height // 2

        # point to which current screen center is transformed after zoom
        old_screen_center_x = pond_center_x + diff_x_after_zoom
        old_screen_center_y = pond_center_y + diff_y_after_zoom

        vals.x_offset += int(screen_center_x - old_screen_center_x)
        vals.y_offset += int(screen_center_y - old_screen_center_y)

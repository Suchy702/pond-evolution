from math import ceil, copysign

from src.events.event import GraphicEvent
from src.events.event_type import GraphicEventType
from src.simulation_settings import SimulationSettings
from src.graphics.graphic_values_guard import GraphicValuesGuard


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
    def _find_pos_to_draw_when_move(event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        x1 = event.from_x * vals.cell_size + vals.x_offset
        y1 = event.from_y * vals.cell_size + vals.y_offset
        x2 = event.to_x * vals.cell_size + vals.x_offset
        y2 = event.to_y * vals.cell_size + vals.y_offset

        if x1 == x2:
            dist = y2 - y1
            y = int(y1 + dist * event.step / event.total_steps)
            x = x1
        else:
            dist = x2 - x1
            a = (y2 - y1) / (x2 - x1)
            b = y1 - a * x1

            x = int(x1 + dist * event.step / event.total_steps)
            y = int(a * x + b)
        return x, y

    @staticmethod
    def _find_pos_to_draw_when_stay(event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        x = int(event.x * vals.cell_size + vals.x_offset)
        y = int(event.y * vals.cell_size + vals.y_offset)
        return x, y

    def find_pos_to_draw(self, event: GraphicEvent, vals: GraphicValuesGuard) -> tuple[int, int]:
        if event.event_type == GraphicEventType.ANIM_MOVE:
            return self._find_pos_to_draw_when_move(event, vals)
        else:
            return self._find_pos_to_draw_when_stay(event, vals)

    # Magic function
    def change_vals_to_zoom(self, change: int, vals: GraphicValuesGuard) -> None:
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
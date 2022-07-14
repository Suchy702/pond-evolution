from src.simulation_settings import SimulationSettings


class GraphicValuesGuard:
    def __init__(self, settings: SimulationSettings):
        self._screen: Surface = pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        self._cell_size: int = CELL_MIN_PX_SIZE  # length of cell's side in px. Cell is a square
        self._x_offset: int = 0
        self._y_offset: int = 0
        self.center_view()

        self._event_emitter = EventEmitter()
from functools import reduce
from typing import cast

from src.object.fish import Fish
from src.object.pond_object import PondObject
from src.object_handler.fish_handler import FishHandler
from src.object_handler.plant_handler import PlantHandler
from src.object_handler.pond_object_handler import PondObjectHandler
from src.object_handler.worm_handler import WormHandler
from src.position import Position
from src.simulation_settings import SimulationSettings


class Interactor:
    def __init__(self, settings: SimulationSettings):
        self._fish_handler: FishHandler = FishHandler(settings)
        self._worm_handler: WormHandler = WormHandler(settings)
        self._plant_handler: PlantHandler = PlantHandler(settings)
        self.handlers: list[PondObjectHandler] = [self._fish_handler, self._worm_handler, self._plant_handler]

    @property
    def all_objects(self) -> list[PondObject]:
        return reduce(lambda list_, handler: list_ + handler.objects, self.handlers, [])

    # beta function for testing
    def preparations(self) -> None:
        for handler in self.handlers:
            handler.add_random(5)

    def _find_pos_where_eat(self) -> list[Position]:
        pos_where_eat = []
        for fish in self._fish_handler.objects:
            if self._worm_handler.is_sth_at_pos(fish.pos) or self._plant_handler.alga_handler.is_sth_at_pos(fish.pos):
                pos_where_eat.append(fish.pos)
        return pos_where_eat

    def _eat_at_one_spot(self, pos: Position) -> None:
        energy_val = self._worm_handler.get_spot_energy_val(pos)
        energy_val += self._plant_handler.alga_handler.get_spot_energy_val(pos)

        for fish in self._fish_handler.get_spot_obj(pos):
            fish = cast(Fish, fish)
            fish.vitality += energy_val // len(self._fish_handler.get_spot_obj(pos))

        self._worm_handler.remove_at_spot(pos)
        self._plant_handler.alga_handler.remove_at_spot(pos)

    def feed_fish(self, pos_where_eat) -> None:
        self._find_pos_where_eat()
        for pos in pos_where_eat:
            self._eat_at_one_spot(pos)

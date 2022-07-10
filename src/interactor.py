from functools import reduce
from typing import cast

from src.constants import HOW_OFTEN_CYCLES_MAKING_WORMS, HOW_OFTEN_CYCLES_MAKING_ALGAE
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
            handler.add_random(10)

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

    def feed_fish(self) -> None:
        for pos in self._find_pos_where_eat():
            self._eat_at_one_spot(pos)

    def remove_unnecessary_objects(self):
        self._fish_handler.remove_dead_fishes()
        self._worm_handler.remove_worms_on_the_ground()
        self._plant_handler.alga_handler.remove_algae_on_surface()

    def _move_food(self) -> None:
        self._worm_handler.move_worms()
        self._plant_handler.move()

    @staticmethod
    def _is_time_to_add_worms(cycle_count: int) -> bool:
        return cycle_count % HOW_OFTEN_CYCLES_MAKING_WORMS == 0

    @staticmethod
    def _is_time_to_detach_algae(cycle_count: int) -> bool:
        return cycle_count % HOW_OFTEN_CYCLES_MAKING_ALGAE == 0

    # Kolejnosc:
    # Jedzenie
    # Rybki
    def move_objects(self) -> None:
        self._move_food()
        self._fish_handler.move_fish()

    def add_new_objects(self, cycle_count: int) -> None:
        if self._is_time_to_add_worms(cycle_count):
            self._worm_handler.add_worms()
        if self._is_time_to_detach_algae(cycle_count):
            self._plant_handler.detach_algae_from_makers()
        self._fish_handler.breed_fish()

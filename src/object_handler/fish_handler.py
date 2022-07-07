from random import randint

from overrides import overrides

from src.constants import FISH_MIN_SPEED, FISH_MAX_SPEED, FISH_MIN_SIZE, FISH_MAX_SIZE
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandler
from src.object.fish import Fish
from src.pond import Pond
from src.simulation_settings import SimulationSettings


class FishHandler(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @overrides
    def create_random_single(self) -> PondObject:
        speed = randint(FISH_MIN_SPEED, FISH_MAX_SPEED)
        size = randint(FISH_MIN_SIZE, FISH_MAX_SIZE)
        return Fish(speed, size, self._pond.random_position())

    # TODO Pycharm wyrzuca blad, PondObject nie ma metody find_pos_to_move, typehinty przeszkadzaja
    def move_fishes(self, pond: Pond) -> None:
        for fish in self._object_database.objects:
            pond.change_position(fish, pond.trim_position(fish.find_pos_to_move()))


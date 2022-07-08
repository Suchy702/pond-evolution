from random import randint
from typing import cast

from overrides import overrides

from src.constants import FISH_MIN_SPEED, FISH_MAX_SPEED, FISH_MIN_SIZE, FISH_MAX_SIZE
from src.object.fish import Fish
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings


class FishHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @overrides
    def create_random_single(self) -> PondObject:
        speed = randint(FISH_MIN_SPEED, FISH_MAX_SPEED)
        size = randint(FISH_MIN_SIZE, FISH_MAX_SIZE)
        return Fish(speed, size, self._pond.random_position())

    # TODO Pycharm wyrzuca blad, PondObject nie ma metody find_pos_to_move, typehinty przeszkadzaja
    def move_fish(self) -> None:
        for fish in self._object_database.objects:
            fish = cast(Fish, fish)
            self._pond.change_position(fish, self._pond.trim_position(fish.find_pos_to_move()))

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

    @property
    def fishes(self) -> list[Fish]:
        return [cast(Fish, fish) for fish in self.objects]

    @overrides
    def create_random_single(self) -> PondObject:
        speed = randint(FISH_MIN_SPEED, FISH_MAX_SPEED)
        size = randint(FISH_MIN_SIZE, FISH_MAX_SIZE)
        return Fish(speed, size, self._pond.random_position())

    def move_fishes(self) -> None:
        for fish in self.fishes:
            self._pond.change_position(fish, self._pond.trim_position(fish.find_pos_to_move()))

    def remove_dead_fishes(self) -> None:
        self.remove_all([fish for fish in self.fishes if fish.is_dead()])

    def spoil_fishes_vitality(self) -> None:
        for fish in self.fishes:
            fish.spoil_vitality()

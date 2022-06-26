from random import randint

from src.pond_object_handler import PondObjectHandler
from src.fish import Fish
from src.pond import Pond

FISH_MIN_SPEED = 5
FISH_MAX_SPEED = 10

FISH_MIN_SIZE = 5
FISH_MAX_SIZE = 10


class FishHandler(PondObjectHandler):
    def __init__(self, pond_height: int, pond_widht: int):
        super().__init__(pond_height, pond_widht)

    @property
    def fishes(self):
        return self._base.objects

    def _create_random_fish(self) -> Fish:
        speed = randint(FISH_MIN_SPEED, FISH_MAX_SPEED)
        size = randint(FISH_MIN_SIZE, FISH_MAX_SIZE)
        return Fish(speed, size, self._pond.random_pos())

    def move_fishes(self, pond: Pond) -> None:
        for fish in self._base.objects:
            pond.change_pos(fish, pond.correct_pos(fish.find_pos_to_move()))

    def add_random_fishes(self, num_of_fishes: int) -> None:
        for _ in range(num_of_fishes):
            self._add(self._create_random_fish())


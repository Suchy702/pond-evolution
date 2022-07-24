import random
from enum import Enum, auto, unique


@unique
class FishTrait(Enum):
    PREDATOR = auto()
    ALTRUISTIC = auto()
    SMART = auto()

    @staticmethod
    def get_random():
        return random.choice(list(FishTrait))

    def __str__(self):
        return self.name

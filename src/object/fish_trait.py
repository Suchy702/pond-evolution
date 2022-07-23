from enum import Enum, auto, unique


@unique
class FishTrait(Enum):
    PREDATOR = auto()
    ALTRUISTIC = auto()
    SMART = auto()

    def __str__(self):
        return self.name

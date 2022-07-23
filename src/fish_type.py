from enum import Enum, auto, unique


@unique
class FishType(Enum):
    HERBIVORE = auto()
    CARNIVORE = auto()
    OMNIVORE = auto()

    def __str__(self):
        return self.name

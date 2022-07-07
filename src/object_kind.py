from enum import Enum, auto, unique


@unique
class ObjectKind(Enum):
    ALGA = auto()
    FISH = auto()
    PLANT = auto()
    WORM = auto()
    MAKER = auto()

    def __str__(self):
        return self.name

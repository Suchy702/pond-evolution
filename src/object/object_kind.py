from enum import Enum, auto, unique


@unique
class ObjectKind(Enum):
    ALGA = auto()
    FISH = auto()
    PLANT = auto()
    WORM = auto()
    ALGA_MAKER = auto()
    FAKE = auto()

    def __str__(self):
        return self.name

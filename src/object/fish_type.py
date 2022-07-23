from enum import Enum, auto, unique


@unique
class FishType(Enum):
    HERBIVORE = auto()
    CARNIVORE = auto()
    OMNIVORE = auto()

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.name

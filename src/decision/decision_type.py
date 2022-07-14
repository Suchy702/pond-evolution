from enum import unique, Enum, auto


@unique
class DecisionType(Enum):
    MOVE = auto()
    STAY = auto()
    DIE = auto()
    REPRODUCE = auto()

    def __str__(self):
        return self.name

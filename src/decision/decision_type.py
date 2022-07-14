from enum import unique, Enum, auto


@unique
class DecisionType(Enum):
    MOVE = auto()
    STAY = auto()
    DIE = auto()
    BREED = auto()
    EAT = auto()

    def __str__(self):
        return self.name

from enum import unique, Enum, auto


class EventType(Enum):
    def __str__(self):
        return self.name


@unique
class LogicEventType(EventType):
    pass


@unique
class GraphicEventType(EventType):
    KEY_PRESSED = auto()

    # ANIMATION
    ANIM_MOVE = auto()
    ANIM_STAY = auto()


@unique
class GameEventType(EventType):
    QUIT = auto()


@unique
class ClickEventType(EventType):
    CHECKING = auto()
    ADDING = auto()

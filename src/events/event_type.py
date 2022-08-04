from enum import unique, Enum, auto


class EventType(Enum):
    def __str__(self):
        return self.name


@unique
class LogicEventType(EventType):
    ADD = auto()


@unique
class GraphicEventType(EventType):
    KEY_PRESSED = auto()

    # ANIMATION
    ANIM_MOVE = auto()
    ANIM_STAY = auto()
    ANIM_NEW = auto()

    # UI
    CHANGE_ADD = auto()


@unique
class GameEventType(EventType):
    QUIT = auto()


@unique
class ClickEventType(EventType):
    LEFT_CLICK = auto()
    RIGHT_CLICK = auto()

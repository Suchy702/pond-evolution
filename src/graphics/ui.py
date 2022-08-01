from src.object.fish import Fish
from src.position import Position


class UI:
    def __init__(self):
        self._adding_object = Fish(10, 10, 3, Position(-1, -1))

    @property
    def adding_object(self):
        return Fish(10, 10, 3, Position(-1, -1))

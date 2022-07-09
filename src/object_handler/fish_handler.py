from itertools import chain
from random import randint
from typing import cast

from overrides import overrides

from src.constants import FISH_MIN_SPEED, FISH_MAX_SPEED, FISH_MIN_SIZE, FISH_MAX_SIZE
from src.events.event import Event, EventType
from src.events.event_manager import EventManager
from src.object.fish import Fish
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.simulation_settings import SimulationSettings

event_manager = EventManager()


class FishHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)

    @property
    def fishes(self) -> list[Fish]:
        return [cast(Fish, fish) for fish in self.objects]

    @overrides
    def create_random_single(self) -> PondObject:
        speed = randint(FISH_MIN_SPEED, FISH_MAX_SPEED)
        size = randint(FISH_MIN_SIZE, FISH_MAX_SIZE)
        return Fish(speed, size, self._pond.random_position())

    def move_fish(self) -> None:
        for fish in self.fishes:
            n_pos = self._pond.trim_position(fish.find_pos_to_move())
            event_manager.emit_event(
                Event(EventType.ANIM_MOVE, object=fish, from_x=fish.pos.x, from_y=fish.pos.y, to_x=n_pos.x,
                      to_y=n_pos.y))
            self._pond.change_position(fish, n_pos)

    def remove_dead_fishes(self) -> None:
        self.remove_all([fish for fish in self.fishes if fish.is_dead()])

    def spoil_fishes_vitality(self) -> None:
        for fish in self.fishes:
            fish.spoil_vitality()

    def breed_fish(self) -> None:
        self.add_all(chain.from_iterable([fish.birth_fish() for fish in self.fishes if fish.is_breeding()]))
        self.remove_all([fish for fish in self.fishes if fish.is_breeding()])

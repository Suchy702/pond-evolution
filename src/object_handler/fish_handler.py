import functools
import itertools
from random import randint, random
from typing import cast, Generator

from overrides import overrides

from src.constants import FISH_MIN_SPEED, FISH_MAX_SPEED, FISH_MIN_SIZE, FISH_MAX_SIZE
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.events.event_type import GraphicEventType
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.object_kind import ObjectKind
from src.pond_viewer import PondViewer
from src.position import Position
from src.simulation_settings import SimulationSettings

event_emitter = EventEmitter()


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
        fish = Fish(speed, size, max(1, self._pond.height // 5), self._pond.random_position())
        if random() < 0.5:
            fish.traits.add(FishTrait.SMART)
        if random() < 0.2:
            fish.traits.add(FishTrait.PREDATOR)
            fish.eyesight = fish.eyesight * 15 // 10
        return fish

    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> Generator[DecisionSet, None, None]:
        sorted_fish = sorted(self.fishes, key=functools.cmp_to_key(self._cmp_by_movement_order))

        for key, group in itertools.groupby(sorted_fish, lambda f: FishTrait.PREDATOR in f.traits):
            decisions = DecisionSet()
            for fish in group:
                if fish.is_alive():
                    decisions += fish.get_decisions(pond_viewer)
            yield decisions

    @staticmethod
    def _cmp_by_movement_order(a: Fish, b: Fish):
        # predators move first
        return (FishTrait.PREDATOR in b.traits) - (FishTrait.PREDATOR in a.traits)

    def handle_decisions(self, decisions: DecisionSet):
        for decision in decisions[DecisionType.MOVE, ObjectKind.FISH]:
            self.move_fish(decision)
        for decision in decisions[DecisionType.STAY, ObjectKind.FISH]:
            self.move_fish(decision, True)
        for decision in decisions[DecisionType.REPRODUCE, ObjectKind.FISH]:
            fish = cast(Fish, decision.pond_object)
            self.breed_fish(fish)

    def move_fish(self, decision: Decision, stay=False) -> None:
        n_pos = self._pond.trim_position(Position(decision.to_y, decision.to_x))
        fish = cast(Fish, decision.pond_object)

        if stay:
            event_emitter.emit_event(
                GraphicEvent(
                    GraphicEventType.ANIM_STAY, pond_object=decision.pond_object,
                    x=decision.pond_object.pos.x, y=decision.pond_object.pos.y
                )
            )
        else:
            event_emitter.emit_event(
                GraphicEvent(
                    GraphicEventType.ANIM_MOVE, pond_object=fish,
                    from_x=fish.pos.x, from_y=fish.pos.y,
                    to_x=n_pos.x, to_y=n_pos.y
                )
            )
            fish.spoil_vitality()

        self._pond.change_position(fish, n_pos)

    def breed_fish(self, fish: Fish) -> None:
        self.add_all(fish.birth_fish())
        self.remove(fish)

    def remove_dead_fish(self) -> None:
        self.remove_all([fish for fish in self.fishes if not fish.is_alive()])

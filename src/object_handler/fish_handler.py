import functools
import itertools
import math
import multiprocessing
from random import randint, random
from typing import cast, Generator, Optional

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
from src.object.fish_type import FishType
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.pond.pond_viewer import PondViewer
from src.position import Position
from src.simulation_settings import SimulationSettings

event_emitter = EventEmitter()


class FishHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self.pool = multiprocessing.Pool(8)

    @property
    def fishes(self) -> list[Fish]:
        return [cast(Fish, fish) for fish in self.objects]

    @overrides
    def create_random_single(self) -> PondObject:
        speed = randint(FISH_MIN_SPEED, FISH_MAX_SPEED)
        size = randint(FISH_MIN_SIZE, FISH_MAX_SIZE)
        fish = Fish(speed, size, max(1, self._pond.height // 5), self._pond.random_position())
        fish.fish_type = FishType.get_random()
        if random() < 0.7:
            fish.traits.add(FishTrait.SMART)
        if random() < 0.2:
            fish.traits.add(FishTrait.PREDATOR)
            if fish.fish_type == FishType.HERBIVORE:
                if random() < 0.5:
                    fish.fish_type = FishType.CARNIVORE
                else:
                    fish.fish_type = FishType.OMNIVORE
        return fish

    @overrides
    def get_decisions(self, pond_viewer: PondViewer) -> Generator[DecisionSet, None, None]:
        sorted_fish = sorted(self.fishes, key=functools.cmp_to_key(self._cmp_by_movement_order))

        for key, group in itertools.groupby(sorted_fish, lambda f: FishTrait.PREDATOR in f.traits):
            decisions = DecisionSet()
            results = self.pool.imap(functools.partial(PondObject.get_decisions, pond_viewer=pond_viewer), group)

            for result in results:
                decisions += result
            yield decisions

    @staticmethod
    def _cmp_by_movement_order(a: Fish, b: Fish):
        # predators move first
        return (FishTrait.PREDATOR in b.traits) - (FishTrait.PREDATOR in a.traits)

    def handle_decisions(self, decisions: DecisionSet):
        for decision in decisions[DecisionType.MOVE, ObjectKind.FISH]:
            self.move_fish(decision)
            self._object_database._object_database[decision.pond_object.id] = decision.pond_object
        for decision in decisions[DecisionType.STAY, ObjectKind.FISH]:
            self.move_fish(decision, True)
            self._object_database._object_database[decision.pond_object.id] = decision.pond_object
        for decision in decisions[DecisionType.REPRODUCE, ObjectKind.FISH]:
            fish = cast(Fish, decision.pond_object)
            self.breed_fish(fish)

    def move_fish(self, decision: Decision, stay=False) -> None:
        fish = cast(Fish, decision.pond_object)

        if stay:
            event_emitter.emit_event(
                GraphicEvent(
                    GraphicEventType.ANIM_STAY, pond_object=decision.pond_object,
                    x=decision.pond_object.pos.x, y=decision.pond_object.pos.y
                )
            )
        else:
            n_pos = self._pond.trim_position(Position(decision.to_y, decision.to_x))
            event_emitter.emit_event(
                GraphicEvent(
                    GraphicEventType.ANIM_MOVE, pond_object=fish,
                    from_x=fish.pos.x, from_y=fish.pos.y,
                    to_x=n_pos.x, to_y=n_pos.y,
                    is_flipped=fish.pos.x <= n_pos.x,
                    rotate=self._get_rotation_angle(n_pos.x - fish.pos.x, fish.pos.y - n_pos.y)
                )
            )
            fish.spoil_vitality()
            self._pond.change_position(fish, n_pos)

    @staticmethod
    def _get_rotation_angle(x: int, y: int) -> Optional[float]:
        if math.isclose(x, 0) and math.isclose(y, 0):
            return None

        degree = math.atan2(y, x) * 180 / math.pi

        if -90 <= degree <= 90:
            return degree
        elif 90 < degree < 180:
            return degree - 180
        return degree + 180

    def breed_fish(self, fish: Fish) -> None:
        self.add_all(fish.birth_fish())
        self.remove(fish)

    def remove_dead_fish(self) -> None:
        self.remove_all([fish for fish in self.fishes if not fish.is_alive()])

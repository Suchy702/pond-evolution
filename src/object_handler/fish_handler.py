from random import randint
from typing import cast

from overrides import overrides

from src.constants import FISH_MIN_SPEED, FISH_MAX_SPEED, FISH_MIN_SIZE, FISH_MAX_SIZE
from src.decision.decision import decisionSetType, Decision
from src.decision.decision_type import DecisionType
from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.events.event_type import GraphicEventType
from src.object.fish import Fish
from src.object.pond_object import PondObject
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.object_kind import ObjectKind
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
        return Fish(speed, size, self._pond.random_position())

    def handle_decisions(self, decisions: decisionSetType):
        if DecisionType.MOVE in decisions and ObjectKind.FISH in decisions[DecisionType.MOVE]:
            for decision in decisions[DecisionType.MOVE][ObjectKind.FISH]:
                self.move_fish(decision)
        if DecisionType.REPRODUCE in decisions and ObjectKind.FISH in decisions[DecisionType.REPRODUCE]:
            for decision in decisions[DecisionType.REPRODUCE][ObjectKind.FISH]:
                self.breed_fish(decision.pond_object)

    def move_fish(self, decision: Decision) -> None:
        n_pos = self._pond.trim_position(Position(decision.to_y, decision.to_x))
        event_emitter.emit_event(
            GraphicEvent(GraphicEventType.ANIM_MOVE, pond_object=decision.pond_object,
                         from_x=decision.pond_object.pos.x, from_y=decision.pond_object.pos.y,
                         to_x=n_pos.x, to_y=n_pos.y
                         )
        )
        self._pond.change_position(decision.pond_object, n_pos)
        decision.pond_object.spoil_vitality()

    def remove_dead_fishes(self) -> None:
        self.remove_all([fish for fish in self.fishes if fish.is_dead()])

    def spoil_fishes_vitality(self) -> None:
        for fish in self.fishes:
            fish.spoil_vitality()

    def breed_fish(self, fish: Fish) -> None:
        self.add_all(fish.birth_fish())
        self.remove(fish)

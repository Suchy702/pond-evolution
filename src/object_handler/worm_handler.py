from random import randint
from typing import cast

from overrides import overrides

from src.constants import WORM_SPAWN_DELAY
from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.object_kind import ObjectKind
from src.object.pond_object import PondObject
from src.object.worm import Worm
from src.object_handler.pond_object_handler import PondObjectHandlerHomogeneous
from src.position import Position
from src.simulation_settings import SimulationSettings


class WormHandler(PondObjectHandlerHomogeneous):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self.worms_from_heaven: bool = not settings.no_worms_from_heaven

    @property
    def worms(self):
        objects = cast(list[Worm], self.objects)
        return objects

    def add_worms(self) -> None:
        if self.worms_from_heaven:
            self.add_all([self.create_random_single() for _ in range(self._choose_worm_amount())])

    @overrides
    def create_random_single(self) -> PondObject:
        position = self._pond.random_position()
        position.y = 0
        return Worm(self.settings.worm_energy, position, self._pond.shape)

    def handle_decisions(self, decisions: DecisionSet):
        for decision in decisions[DecisionType.MOVE, ObjectKind.WORM]:
            self.move_worm(decision)
        if decisions[DecisionType.REPRODUCE, ObjectKind.WORM]:
            self.add_worms()

    def move_worm(self, decision: Decision) -> None:
        new_position = self._pond.trim_position(Position(decision.to_y, decision.to_x))
        self.event_emitter.emit_anim_move_event(decision, new_position)
        self._pond.change_position(decision.pond_object, new_position)

    def remove_worms_on_ground(self) -> None:
        self.remove_all([worm for worm in self.worms if self._pond.is_on_ground(worm.position)])

    def _choose_worm_amount(self):
        min_, max_ = self.settings.worm_intensity, int(self.settings.worm_intensity*1.5)
        return randint(min_, max_)

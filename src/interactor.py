from __future__ import annotations

from functools import reduce
from typing import cast, Type, Generator

from src.ai.ai import AI
from src.ai.alga_ai import AlgaAI
from src.ai.alga_maker_ai import AlgaMakerAI
from src.ai.fish_ai import FishAI
from src.ai.worm_ai import WormAI
from src.decision.decision_set import DecisionSet
from src.events.event_emitter import EventEmitter
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.pond_object import PondObject
from src.object_handler.fish_handler import FishHandler
from src.object_handler.plant_handler import PlantHandler
from src.object_handler.pond_object_handler import PondObjectHandler
from src.object_handler.worm_handler import WormHandler
from src.pond_viewer import PondViewer
from src.position import Position
from src.simulation_settings import SimulationSettings

event_emitter = EventEmitter()


class Interactor:
    def __init__(self, settings: SimulationSettings):
        self._fish_handler: FishHandler = FishHandler(settings)
        self._worm_handler: WormHandler = WormHandler(settings)
        self._plant_handler: PlantHandler = PlantHandler(settings)
        # order of handlers and AI classes is important
        self.handlers: list[PondObjectHandler] = [self._plant_handler, self._worm_handler, self._fish_handler]
        self.ai_classes: list[Type[AI] | tuple[Type[AI], ...]] = [(AlgaAI, AlgaMakerAI), WormAI, FishAI]

        self.pond_viewer = PondViewer(settings.pond_width, settings.pond_height)
        for handler in self.handlers:
            self.pond_viewer.add_ponds(handler.ponds)

    @property
    def all_objects(self) -> list[PondObject]:
        return reduce(lambda list_, handler: list_ + handler.objects, self.handlers, [])  # type: ignore

    def _get_decisions(self) -> Generator[DecisionSet, None, None]:
        for idx, (handler, ai_classes) in enumerate(zip(self.handlers, self.ai_classes)):
            if type(ai_classes) is tuple:
                for ai in ai_classes:
                    yield ai.get_general_decisions(), idx
            else:
                yield ai_classes.get_general_decisions(), idx
            for decisions in handler.get_decisions(self.pond_viewer):
                yield decisions, idx

    def handle_decisions(self) -> None:
        for decisions, handler_idx in self._get_decisions():
            self.handlers[handler_idx].handle_decisions(decisions)
            self._handle_decisions(decisions)

    def _handle_decisions(self, decisions: DecisionSet) -> None:
        pass

    # beta function for testing
    def preparations(self) -> None:
        self._plant_handler.add_random(10)
        self._fish_handler.add_random(100)

    def _find_pos_where_eat(self) -> list[Position]:
        pos_where_eat = []
        for fish in self._fish_handler.fishes:
            if self._worm_handler.is_sth_at_pos(fish.pos) or self._plant_handler.alga_handler.is_sth_at_pos(
                    fish.pos) or (
                    FishTrait.PREDATOR in fish.traits and len(self._fish_handler.get_spot_obj(fish.pos)) > 1):
                pos_where_eat.append(fish.pos)
        return pos_where_eat

    def _eat_at_spot(self, pos: Position) -> None:
        self.eat_other_non_fish_at_spot(pos)
        self.eat_other_fish_at_spot(pos)

    def eat_other_non_fish_at_spot(self, pos: Position) -> None:
        energy_val = self._worm_handler.get_spot_energy_val(pos)
        energy_val += self._plant_handler.alga_handler.get_spot_energy_val(pos)

        for fish in self._fish_handler.get_spot_obj(pos):
            fish = cast(Fish, fish)
            fish.vitality += energy_val // len(self._fish_handler.get_spot_obj(pos))

        self._worm_handler.remove_at_spot(pos)
        self._plant_handler.alga_handler.remove_at_spot(pos)

    def eat_other_fish_at_spot(self, pos: Position) -> None:
        fish = self._fish_handler.get_spot_obj(pos)
        predator_cnt, predator_energy_val = 0, 0
        energy_val = self._fish_handler.get_spot_energy_val(pos)

        for f in fish:
            f = cast(Fish, f)
            if FishTrait.PREDATOR in f.traits:
                predator_energy_val += f.energy_val
                predator_cnt += 1

        if predator_cnt == 0:
            return

        for f in fish:
            f = cast(Fish, f)
            if FishTrait.PREDATOR in f.traits:
                f.vitality += (energy_val - predator_energy_val) // predator_cnt
            else:
                f.is_eaten = True

    # TODO:  mark eaten fish as dead
    def feed_fish(self) -> None:
        for pos in self._find_pos_where_eat():
            self._eat_at_spot(pos)

    def remove_unnecessary_objects(self) -> None:
        self._fish_handler.remove_dead_fish()
        self._worm_handler.remove_worms_on_the_ground()
        self._plant_handler.alga_handler.remove_algae_on_surface()

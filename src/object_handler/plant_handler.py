from overrides import overrides

from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject
from src.object_handler.alga_handler import AlgaHandler
from src.object_handler.alga_maker_handler import AlgaMakerHandler
from src.object_handler.pond_object_handler import PondObjectHandlerBundler
from src.object_kind import ObjectKind
from src.position import Position
from src.simulation_settings import SimulationSettings


class PlantHandler(PondObjectHandlerBundler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self.alga_handler: AlgaHandler = AlgaHandler(settings)
        self.alga_maker_handler: AlgaMakerHandler = AlgaMakerHandler(settings)

        self._handlers.extend([self.alga_handler, self.alga_maker_handler])

    def handle_decisions(self, decisions: DecisionSet):
        self.alga_handler.handle_decisions(decisions)
        self.alga_maker_handler.handle_decisions(decisions)

        for decision in decisions[DecisionType.REPRODUCE, ObjectKind.ALGA_MAKER]:
            self.detach_algae_from_maker(decision.pond_object)

    @overrides
    def add_random(self, amount: int) -> None:
        self.alga_handler.add_random(amount)
        self.alga_maker_handler.add_random(amount)

    @overrides
    def get_spot_obj(self, pos: Position) -> set[PondObject]:
        return self.alga_handler.get_spot_obj(pos) | self.alga_maker_handler.get_spot_obj(pos)

    def detach_algae_from_maker(self, maker: AlgaMaker) -> None:
        self.alga_handler.add_all(self.alga_maker_handler.create_algae(maker))

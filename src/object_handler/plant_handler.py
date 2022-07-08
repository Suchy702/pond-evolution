from overrides import overrides

from src.object_handler.alga_handler import AlgaHandler
from src.object_handler.alga_maker_handler import AlgaMakerHandler
from src.object_handler.pond_object_handler import PondObjectHandlerBundler
from src.simulation_settings import SimulationSettings


class PlantHandler(PondObjectHandlerBundler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self.alga_handler: AlgaHandler = AlgaHandler(settings)
        self.alga_maker_handler: AlgaMakerHandler = AlgaMakerHandler(settings)

        self._handlers.extend([self.alga_handler, self.alga_maker_handler])

    @overrides
    def add_random(self, amount: int) -> None:
        self.alga_handler.add_random(amount)
        self.alga_maker_handler.add_random(amount)

    # TODO: type hintsy sie wala
    def detach_algs_from_alg_makers(self) -> None:
        for alg_maker in self.alga_maker_handler.objects:
            self.alga_handler.add_all(_make_algae_with_alga_maker(self.alga_handler, alg_maker))

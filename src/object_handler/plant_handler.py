from src.object.pond_object import PondObject
from src.object_handler.alga_handler import AlgaHandler
from src.object_handler.alga_maker_handler import AlgaMakerHandler
from src.object.alga_maker import AlgaMaker
from src.object.alga import Alga
from src.object_handler.pond_object_handler import PondObjectHandler
from src.simulation_settings import SimulationSettings

# TODO tu nie powinno byc dziedziczenia
class PlantHandler(PondObjectHandler):
    def __init__(self, settings: SimulationSettings):
        super().__init__(settings)
        self.alga_handler: AlgaHandler = AlgaHandler(settings)
        self.alga_maker_handler: AlgaMakerHandler = AlgaMakerHandler(settings)

    def create_random_single(self) -> PondObject:
        return self.alga_maker_handler.create_random_single()

    # TODO: znowu wywalaja type hintsy, przez override funkcji, no i Pycharm szaleje ze range nie moze przyjac int xD
    def _make_algs_by_alg_maker(self, alg_maker: AlgaMaker) -> list[Alga]:
        return [self.alga_handler.create_random_single(alg_maker.pos) for _ in range(alg_maker.choose_algae_amount)]

    # TODO: type hintsy sie wala
    def detach_algs_from_alg_makers(self) -> None:
        for alg_maker in self.alga_maker_handler.objects:
            self.alga_handler.add_all(self._make_algs_by_alg_maker(alg_maker))

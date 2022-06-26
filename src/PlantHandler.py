from src.algae_handler import AlgaeHandler
from src.algae_maker_handler import AlgaeMakerHandler
from src.algae_maker import AlgaeMaker
from src.algae import Algae


class PlantHandler:
    def __init__(self, pond_height: int, pond_width: int):
        self.alg_handler: AlgaeHandler = AlgaeHandler(pond_height, pond_width)
        self.alg_maker_handler: AlgaeMakerHandler = AlgaeMakerHandler(pond_height, pond_width)

    def _make_algs_by_alg_maker(self, alg_maker: AlgaeMaker) -> list[Algae]:
        return [self.alg_handler.create_alg(alg_maker.pos) for _ in range(alg_maker.created_algs_amonut)]

    def detach_algs_from_alg_makers(self) -> None:
        for alg_maker in self.alg_maker_handler.alg_makers:
            self.alg_handler.add_many(self._make_algs_by_alg_maker(alg_maker))

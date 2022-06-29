from src.algae_maker import AlgaeMaker
from src.pond_object_handler import PondObjectHandler
from src.position import Position


class AlgaeMakerHandler(PondObjectHandler):
    def __init__(self, pond_height: int, pond_width: int):
        super().__init__(pond_height, pond_width)

    @property
    def alg_makers(self):
        return self._base.objects

    def _create_random_alg_maker(self) -> AlgaeMaker:
        return AlgaeMaker(Position(self._pond.height-1, self._pond.random_pos().x))

    def plant_alg_makers(self, num_of_alg_makers: int) -> None:
        self.add_all([self._create_random_alg_maker() for _ in range(num_of_alg_makers)])

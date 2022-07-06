from src.pond_object_handler import PondObjectHandler
from src.position import Position
from src.algae import Algae

ALGAE_ENERGY_VAL = 15


class AlgaeHandler(PondObjectHandler):
    def __init__(self, pond_height: int, pond_width: int):
        super().__init__(pond_height, pond_width)

    @property
    def algs(self):
        return self._base.objects

    def create_alg(self, pos: Position) -> Algae:
        return Algae(ALGAE_ENERGY_VAL, pos, self._pond.height)

    def move_algs(self) -> None:
        for algae in self.algs:
            self._pond.change_pos(algae, self._pond.correct_pos(algae))

    def del_algs_on_surface(self) -> None:
        to_del = []
        for alg in self.algs:
            if self._pond.is_on_surface(alg.pos):
                to_del.append(alg)
        self.remove_all(to_del)

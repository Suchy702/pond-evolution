from src.worm import Worm
from src.pond_object_handler import PondObjectHandler
from src.position import Position

WORM_ENERGY_VAL = 15


class WormHandler(PondObjectHandler):
    def __init__(self, pond_height: int, pond_width: int):
        super().__init__(pond_height, pond_width)

    @property
    def worms(self):
        return self._base.objects

    def _create_random_worm(self) -> Worm:
        return Worm(WORM_ENERGY_VAL, Position(0, self._pond.random_pos().x), self._pond.dimensions)

    def send_worms(self, num_of_worms: int) -> None:
        self.add_all([self._create_random_worm() for _ in range(num_of_worms)])

    def move_worms(self) -> None:
        for worm in self.worms:
            self._pond.change_pos(worm, self._pond.correct_pos(worm.find_pos_to_move))

    def del_worms_from_the_ground(self) -> None:
        to_del = []
        for worm in self.worms:
            if self._pond.is_on_the_ground(worm.pos):
                to_del.append(worm)
        self.remove_all(to_del)

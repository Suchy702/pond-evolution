from src.worm_handler import WormHandler
from src.plant_handler import PlantHandler
from src.fish_handler import FishHandler
from src.position import Position

POND_HEIGHT = 5
POND_WIDTH = 10

class Engine:
    def __init__(self):
        self.fish_h: FishHandler = FishHandler(POND_HEIGHT, POND_WIDTH)
        self.worm_h: WormHandler = WormHandler(POND_HEIGHT, POND_WIDTH)
        self.plant_h: PlantHandler = PlantHandler(POND_HEIGHT, POND_WIDTH)

    @property
    def all_objects(self):
        return self.fish_h.fishes+self.worm_h.worms+self.plant_h.plants

    def find_pos_where_eat(self) -> list[Position]:
        pos_where_eat = []
        for fish in self.fish_h.fishes:
            if self.worm_h.is_sth_at_pos(fish.pos) or self.plant_h.alg_handler.is_sth_at_pos(fish.pos):
                pos_where_eat.append(fish.pos)
        return pos_where_eat

    def eat_at_one_pos(self, pos: Position) -> None:
        energy_val = sum(self.worm_h.get_spot_obj(pos)) + sum(self.plant_h.alg_handler.get_spot_obj(pos))
        for fish in self.fish_h.get_spot_obj(pos):
            fish.energy += energy_val // len(self.fish_h.get_spot_obj(pos))
        self.worm_h.remove_at_spot(pos)
        self.plant_h.alg_handler.remove_at_spot(pos)

    def feed_fish(self, pos_where_eat) -> None:
        for pos in pos_where_eat:
            self.eat_at_one_pos(pos)

    def preparations(self) -> None:
        self.fish_h.add_random_fishes(5)
        self.worm_h.send_worms(5)
        self.plant_h.alg_maker_handler.plant_alg_makers(5)

    def show_pond(self) -> None:
        self.preparations()
        board: list[list[list[str]]] = [[[] for _ in range(POND_WIDTH)] for _ in range(POND_HEIGHT)]
        for obj in self.all_objects:
            board[obj.pos.y][obj.pos.x].append(str(obj))
        for row in board:
            print(row)

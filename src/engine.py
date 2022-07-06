from src.worm_handler import WormHandler
from src.plant_handler import PlantHandler
from src.fish_handler import FishHandler


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

    def preparations(self):
        self.fish_h.add_random_fishes(5)
        self.worm_h.send_worms(5)
        self.plant_h.alg_maker_handler.plant_alg_makers(5)

    def show_pond(self):
        self.preparations()
        board: list[list[list[str]]] = [[[] for _ in range(POND_WIDTH)] for _ in range(POND_HEIGHT)]
        for obj in self.all_objects:
            board[obj.pos.y][obj.pos.x].append(str(obj))
        for row in board:
            print(row)

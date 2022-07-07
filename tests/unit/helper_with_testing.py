from src.position import Position
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.worm import Worm
from src.object.fish import Fish


def get_object(kind='F', pos=Position(0, 0), speed=10, size=10, energy_val=15, pond_dim=(90, 160)):
    objects = {'F': Fish(speed, size, pos),
               'W': Worm(energy_val, pos, pond_dim),
               'A': Alga(energy_val, pos, pond_dim[0]),
               'M': AlgaMaker(pos),
               }
    return objects[kind]

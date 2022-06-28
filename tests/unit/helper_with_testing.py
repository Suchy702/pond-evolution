from src.position import Position
from src.algae import Algae
from src.algae_maker import AlgaeMaker
from src.worm import Worm
from src.fish import Fish


def get_object(kind='F', pos=Position(0, 0), speed=10, size=10, energy_val=15, pond_dim=(90, 160)):
    objects = {'F': Fish(speed, size, pos),
               'W': Worm(energy_val, pos, pond_dim),
               'A': Algae(energy_val, pos, pond_dim[0]),
               'M': AlgaeMaker(pos),
               }
    return objects[kind]

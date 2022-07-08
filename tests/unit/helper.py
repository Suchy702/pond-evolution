from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.fish import Fish
from src.object.worm import Worm
from src.object_kind import ObjectKind
from src.position import Position


def get_object(kind=ObjectKind.FISH, pos=Position(0, 0), speed=10, size=10, energy_val=15, pond_dim=(90, 160)):
    objects = {
        ObjectKind.FISH: Fish(speed, size, pos),
        ObjectKind.WORM: Worm(energy_val, pos, pond_dim),
        ObjectKind.ALGA: Alga(energy_val, pos, pond_dim[0]),
        ObjectKind.ALGA_MAKER: AlgaMaker(pos),
    }
    return objects[kind]

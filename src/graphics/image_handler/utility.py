from pygame.surface import Surface

from src.graphics.image_handler.fish_image_handler import FishImageHandler
from src.graphics.image_handler.plant_image_handler import PlantImageHandler
from src.graphics.image_handler.worm_image_handler import WormImageHandler
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.fish import Fish
from src.object.pond_object import PondObject
from src.object.worm import Worm

fish_image_handler = FishImageHandler()
worm_image_handler = WormImageHandler()
plant_image_handler = PlantImageHandler()


def get_object_image(obj: PondObject, size: int) -> Surface:
    if isinstance(obj, Fish):
        return fish_image_handler.get_object_image(obj, size)
    elif isinstance(obj, Worm):
        return worm_image_handler.get_object_image(obj, size)
    elif isinstance(obj, Alga) or isinstance(obj, AlgaMaker):
        return plant_image_handler.get_object_image(obj, size)
    else:
        raise Exception("Unknown object type")

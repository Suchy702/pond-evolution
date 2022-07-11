from pygame.surface import Surface

from src.graphics.image_handler.fish_image_handler import FishImageHandler
from src.graphics.image_handler.plant_image_handler import PlantImageHandler
from src.graphics.image_handler.worm_image_handler import WormImageHandler
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.fish import Fish
from src.object.pond_object import PondObject
from src.object.worm import Worm


def get_object_image(obj: PondObject) -> Surface:
    if isinstance(obj, Fish):
        return FishImageHandler.get_object_image(obj)
    elif isinstance(obj, Worm):
        return WormImageHandler.get_object_image(obj)
    elif isinstance(obj, Alga) or isinstance(obj, AlgaMaker):
        return PlantImageHandler.get_object_image(obj)
    else:
        raise Exception("Unknown object type")

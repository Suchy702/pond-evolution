from pygame.surface import Surface

from src.graphics.image_handler.fish_image_handler import FishImageHandler
from src.graphics.image_handler.plant_image_handler import PlantImageHandler
from src.graphics.image_handler.ui_image_handler import UIImageHandler
from src.graphics.image_handler.worm_image_handler import WormImageHandler
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.fish import Fish
from src.object.pond_object import PondObject
from src.object.worm import Worm


class ImageLoader:
    def __init__(self, static_size: int):
        self.fish_image_handler: FishImageHandler = FishImageHandler()
        self.worm_image_handler: WormImageHandler = WormImageHandler()
        self.plant_image_handler: PlantImageHandler = PlantImageHandler()
        self.ui_image_handler: UIImageHandler = UIImageHandler(static_size)

    def get_object_image(self, obj: PondObject, size: int) -> Surface:
        if isinstance(obj, Fish):
            return self.fish_image_handler.get_object_image(obj, size)
        elif isinstance(obj, Worm):
            return self.worm_image_handler.get_object_image(obj, size)
        elif isinstance(obj, Alga) or isinstance(obj, AlgaMaker):
            return self.plant_image_handler.get_object_image(obj, size)
        else:
            raise Exception("Unknown object type")

    def get_ui_image(self, name: str) -> Surface:
        return self.ui_image_handler.get_static_image(name)

from src.graphics.image_handler.fish_image_handler import FishImageHandler
from src.graphics.image_handler.image_handler import ImageHandler
from src.graphics.image_handler.plant_image_handler import PlantImageHandler
from src.graphics.image_handler.worm_image_handler import WormImageHandler
from src.object_handler.fish_handler import FishHandler
from src.object_handler.plant_handler import PlantHandler
from src.object_handler.pond_object_handler import PondObjectHandler
from src.object_handler.worm_handler import WormHandler


def get_image_handlers(handlers: list[PondObjectHandler]) -> list[ImageHandler]:
    image_handlers = []
    for handler in handlers:
        if isinstance(handler, FishHandler):
            image_handlers.append(FishImageHandler(handler))
        elif isinstance(handler, PlantHandler):
            image_handlers.append(PlantImageHandler(handler))
        elif isinstance(handler, WormHandler):
            image_handlers.append(WormImageHandler(handler))
        else:
            raise Exception("Unknown handler")
    return image_handlers

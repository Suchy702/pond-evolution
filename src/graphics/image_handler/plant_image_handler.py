import os.path

import pygame
from overrides import overrides
from pygame.surface import Surface

from src.graphics.image_handler.image_handler import ImageHandler, IMG_DIR_PATH
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.pond_object import PondObject


class PlantImageHandler(ImageHandler):
    _alga_maker_cache: Surface = None
    _alga_cache: Surface = None

    @staticmethod
    @overrides
    def get_object_image(obj: PondObject) -> Surface:
        if PlantImageHandler._alga_maker_cache is None:
            PlantImageHandler._alga_maker_cache = pygame.image.load(
                os.path.join(IMG_DIR_PATH, 'seaweed.svg')).convert_alpha()
        if PlantImageHandler._alga_cache is None:
            PlantImageHandler._alga_cache = pygame.image.load(os.path.join(IMG_DIR_PATH, 'alga.svg')).convert_alpha()

        if isinstance(obj, AlgaMaker):
            return PlantImageHandler._alga_maker_cache
        elif isinstance(obj, Alga):
            return PlantImageHandler._alga_cache
        else:
            raise Exception('Unknown object type')

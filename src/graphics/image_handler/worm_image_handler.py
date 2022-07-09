import os

import pygame
from overrides import overrides
from pygame.surface import Surface

from src.graphics.image_handler.image_handler import ImageHandler, IMG_DIR_PATH
from src.object.pond_object import PondObject


class WormImageHandler(ImageHandler):
    _cache: Surface = None

    @staticmethod
    @overrides
    def get_object_image(obj: PondObject) -> Surface:
        if WormImageHandler._cache is None:
            WormImageHandler._cache = pygame.image.load(os.path.join(IMG_DIR_PATH, 'worm.svg')).convert_alpha()
        return WormImageHandler._cache

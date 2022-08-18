from __future__ import annotations

import os.path
from abc import ABC, abstractmethod
from typing import ClassVar, Optional

import pygame
from pygame.surface import Surface

from src.constants import CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE
from src.object.pond_object import PondObject

IMG_PATH_DIR = os.path.join('resources', 'img')


class ImageHandler(ABC):
    image_paths: ClassVar[list[str]] = []


class DynamicImageHandler(ImageHandler):
    def __init__(self):
        self._base_image: dict[str, Surface] = {}
        self._cache: dict[str, list[Optional[Surface]]] = {}

        for image_path in self.__class__.image_paths:
            self._base_image[image_path] = pygame.image.load(os.path.join(IMG_PATH_DIR, image_path)).convert_alpha()
            self._cache[image_path] = [None for _ in range(CELL_MAX_PX_SIZE - CELL_MIN_PX_SIZE + 100)]

    def get_object_image(self, object_: PondObject, size: int) -> Surface:
        image_name = self._choose_image(object_)
        return self._load_image(image_name, size)

    @abstractmethod
    def _choose_image(self, object_: PondObject) -> str:
        pass

    def _load_image(self, name: str, size: int) -> Surface:
        if name not in self._cache:
            self._cache[name] = []

        if self._cache[name][size - CELL_MIN_PX_SIZE] is None:
            surface = self._base_image[name]
            self._cache[name][size - CELL_MIN_PX_SIZE] = pygame.transform.smoothscale(surface, (size, size))

        return self._cache[name][size - CELL_MIN_PX_SIZE]


class StaticImageHandler(ImageHandler):
    def __init__(self, size: int):
        self._base_image: dict[str, Surface] = {}

        for image_path in self.__class__.image_paths:
            loaded_img = pygame.image.load(os.path.join(IMG_PATH_DIR, image_path))
            self._base_image[image_path] = pygame.transform.smoothscale(loaded_img, (size, size))

    def get_static_image(self, name: str) -> Surface:
        return self._base_image[f'{name}.svg']

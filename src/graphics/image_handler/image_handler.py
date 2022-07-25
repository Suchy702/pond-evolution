from __future__ import annotations

import os.path
from abc import ABC, abstractmethod
from typing import ClassVar, Optional

import pygame
from pygame.surface import Surface

from src.constants import CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE
from src.object.pond_object import PondObject


class ImageHandler(ABC):
    img_paths: ClassVar[list[str]] = []


class DynamicImageHandler(ImageHandler):
    def __init__(self, img_dir_path: str):
        self._base_image: dict[str, Surface] = {}
        self._cache: dict[str, list[Optional[Surface]]] = {}

        for img_path in self.__class__.img_paths:
            self._base_image[img_path] = pygame.image.load(os.path.join(img_dir_path, img_path))
            self._cache[img_path] = [None for _ in range(CELL_MAX_PX_SIZE - CELL_MIN_PX_SIZE + 1)]

    @abstractmethod
    def _choose_image(self, obj: PondObject) -> str:
        pass

    def _load_image(self, name: str, size: int) -> Surface:
        if name not in self._cache:
            self._cache[name] = []

        if self._cache[name][size - CELL_MIN_PX_SIZE] is None:
            self._cache[name][size - CELL_MIN_PX_SIZE] = pygame.transform.smoothscale(self._base_image[name],
                                                                                      (size, size))

        return self._cache[name][size - CELL_MIN_PX_SIZE]

    def get_object_image(self, obj: PondObject, size: int) -> Surface:
        img_name = self._choose_image(obj)
        return self._load_image(img_name, size)


class StaticImageHandler(ImageHandler):
    def __init__(self, img_dir_path: str, size: int):
        self._base_image: dict[str, Surface] = {}

        for img_path in self.__class__.img_paths:
            loaded_img = pygame.image.load(os.path.join(img_dir_path, img_path))
            self._base_image[img_path] = pygame.transform.smoothscale(loaded_img, (size, size))

    def get_static_image(self, name: str) -> Surface:
        return self._base_image[f'{name}.svg']

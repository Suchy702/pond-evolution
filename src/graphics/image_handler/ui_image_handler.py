from typing import ClassVar

from src.graphics.image_handler.image_handler import StaticImageHandler


class UIImageHandler(StaticImageHandler):
    image_paths: ClassVar[list[str]] = [
        'panel_0.svg', 'panel_3.svg', 'panel_4.svg', 'panel_5.svg', 'panel_7.svg', 'panel_8.svg', 'panel_10.svg',
        'panel_11.svg',
    ]

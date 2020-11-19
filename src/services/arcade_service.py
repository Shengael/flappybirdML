from typing import NewType

import arcade
from arcade import Sprite

FSprite = NewType('Sprite', Sprite)


class ArcadeService:
    @staticmethod
    def load_sprite(path):
        return arcade.Sprite(path, 0.5)

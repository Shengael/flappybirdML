from arcade import SpriteList

from resources.flappy_types import Goals
from resources.sprite_path import Sprites
from src.entities.pipe import Pipe
from src.services.arcade_service import ArcadeService


class TextureManager:
    def __init__(self):
        top_texture = ArcadeService.load_sprite(Sprites.top, 0.5)
        bottom_texture = ArcadeService.load_sprite(Sprites.bottom, 0.5)
        pipe_texture = ArcadeService.load_sprite(Sprites.pipe, 1)
        self.texture = {
            "top": {"height": top_texture.height, "width": top_texture.width},
            "bottom": {"height": bottom_texture.height, "width": bottom_texture.width},
            "pipe": {"height": pipe_texture.height, "width": pipe_texture.width}
        }

    def create_top(self, max_width: int, max_height: int, walls: SpriteList) -> SpriteList:
        quantity = int(max_width / self.texture["top"]["width"]) + 1

        for s in range(quantity):
            sprite = ArcadeService.load_sprite(Sprites.top, 0.5)
            sprite.center_x = sprite.width * 0.5 + sprite.width * s
            sprite.center_y = max_height - (sprite.height * 0.5)
            walls.append(sprite)

        return walls

    def create_bottom(self, max_width: int, walls: SpriteList) -> SpriteList:
        quantity = int(max_width / self.texture["bottom"]["width"]) + 1

        for s in range(quantity):
            sprite = ArcadeService.load_sprite(Sprites.bottom, 0.5)
            sprite.center_x = sprite.width * 0.5 + sprite.width * s
            sprite.center_y = sprite.height * 0.5
            walls.append(sprite)
        return walls

    @staticmethod
    def create_pipes(walls: SpriteList, goals: Goals) -> SpriteList:
        for pipe in goals:
            sprite = ArcadeService.load_sprite(Sprites.pipe, 1)
            sprite.height = max(sprite.height, pipe.height_top)
            top_y = pipe.top + (sprite.height * 0.5)
            sprite.center_x = pipe.position_x + sprite.width * 0.5
            sprite.center_y = top_y
            sprite.angle = 180
            walls.append(sprite)

            sprite = ArcadeService.load_sprite(Sprites.pipe, 1)
            sprite.height = max(sprite.height, pipe.height_bottom)
            bottom_y = pipe.bottom - (sprite.height * 0.5)
            sprite.center_x = pipe.position_x + sprite.width * 0.5
            sprite.center_y = bottom_y
            walls.append(sprite)
        return walls

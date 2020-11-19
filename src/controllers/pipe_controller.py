from resources.env import MIN_PIPE_SIZE, GAP_SIZE, NO_PIPE, ABOVE, UNDER, IN, CHEAT_REWARD
from src.controllers.texture_manager import TextureManager
from src.entities.pipe import Pipe
from src.entities.bird import Bird
from src.services.random_service import RandomService


class PipeController:

    def __init__(self):
        self.texture = TextureManager().texture

    @staticmethod
    def position_player_pipe(pipe: Pipe, bird: Bird, height: int) -> str:
        if pipe is None:
            if CHEAT_REWARD and bird.sprite.center_y > height / 2:
                return ABOVE
            if CHEAT_REWARD and bird.sprite.center_y < height / 2:
                return UNDER
            return NO_PIPE
        if bird.sprite.center_y > pipe.center_y:
            return ABOVE
        if bird.sprite.center_y < pipe.center_y:
            return UNDER
        return IN

    def in_checkpoint(self, pipe: Pipe, bird: Bird) -> bool:
        if pipe.position_x + self.texture["pipe"]["width"] <= bird.get_min_x() \
                and pipe.bottom < bird.get_bottom() and bird.get_top() < pipe.top:
            return True
        return False

    def in_pipe(self, pipe: Pipe, bird: Bird) -> bool:
        if pipe.position_x <= bird.get_max_x() \
                and pipe.position_x + self.texture["pipe"]["width"] >= bird.get_min_x() \
                and (pipe.bottom >= bird.get_bottom() or bird.get_top() >= pipe.top):
            return True
        return False

    @staticmethod
    def distance_checkpoint(pipe: Pipe, bird: Bird, height: int) -> float:
        if pipe is None:
            if CHEAT_REWARD and bird.sprite.center_y > height / 2:
                return bird.sprite.center_y - (height / 2) + 1
            if CHEAT_REWARD and bird.sprite.center_y < height / 2:
                return (height / 2) - bird.sprite.center_y + 1
            return -1
        if bird.sprite.center_y > pipe.center_y:
            return bird.sprite.center_y - pipe.center_y + 1
        if bird.sprite.center_y < pipe.center_y:
            return pipe.center_y - bird.sprite.center_y + 1
        return 0

    @staticmethod
    def create_pipe(position_x: int, max_height: int) -> Pipe:
        top_pipe = RandomService.randint(MIN_PIPE_SIZE + GAP_SIZE, max_height - MIN_PIPE_SIZE - 1)
        bottom_pipe = top_pipe - GAP_SIZE

        return Pipe(bottom_pipe, top_pipe, position_x - 1)

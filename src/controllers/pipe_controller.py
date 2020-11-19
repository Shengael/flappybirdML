from resources.env import MIN_PIPE_SIZE, GAP_SIZE, NO_PIPE, ABOVE, UNDER, IN
from src.entities.pipe import Pipe
from src.entities.bird import Bird
from src.services.random_service import RandomService


class PipeController:
    @staticmethod
    def position_player_pipe(pipe: Pipe, bird: Bird) -> str:
        if pipe is None:
            return NO_PIPE
        if bird.get_top() >= pipe.top:
            return ABOVE
        if bird.get_bottom() <= pipe.bottom:
            return UNDER
        return IN

    @staticmethod
    def in_checkpoint(pipe: Pipe, bird: Bird) -> bool:
        if pipe.position_x == bird.get_position_x() and pipe.bottom < bird.get_bottom() and bird.get_top() < pipe.top:
            return True
        return False

    @staticmethod
    def in_pipe(pipe: Pipe, bird: Bird) -> bool:
        if pipe.position_x == bird.get_position_x() and pipe.bottom >= bird.get_bottom() and bird.get_top() >= pipe.top:
            return True
        return False

    @staticmethod
    def distance_checkpoint(pipe: Pipe, bird: Bird) -> float:
        if bird.get_top() >= pipe.top:
            return pipe.top - bird.get_top() + 1
        if bird.get_bottom() <= pipe.bottom:
            return bird.get_bottom() - pipe.bottom + 1
        return 0

    @staticmethod
    def create_pipe(position_x: int, max_height: int) -> Pipe:
        top_pipe = RandomService.randint(MIN_PIPE_SIZE + 1, max_height - 1 - MIN_PIPE_SIZE - GAP_SIZE)
        bottom_pipe = top_pipe + GAP_SIZE

        return Pipe(bottom_pipe, top_pipe, position_x - 1)

from typing import List

from resources.env import PIPE_FREQUENCY, PIPE_SPEED
from src.controllers.texture_manager import TextureManager
from src.entities.bird import Bird
from src.entities.board import Board
from src.controllers.pipe_controller import PipeController
from src.entities.pipe import Pipe


class BoardController:
    def __init__(self, width: int, height: int) -> None:
        self.board = Board(width, height)
        self.goals: List[Pipe] = []
        self.frequency = 1
        self.texture_manager = TextureManager()
        self.pipe_controller = PipeController()

    def is_bottom(self, bird: Bird) -> bool:
        return bird.get_bottom() < self.texture_manager.texture["bottom"]["height"] - bird.sprite.height * 0.5

    def is_top(self, bird: Bird) -> bool:
        return bird.get_top() >= self.board.height - self.texture_manager.texture["top"]["height"]

    def is_pipe(self, bird: Bird) -> bool:
        return len(self.goals) != 0 and self.pipe_controller.in_pipe(self.goals[0], bird)

    def is_checkpoint(self, bird: Bird) -> bool:
        return len(self.goals) != 0 and self.pipe_controller.in_checkpoint(self.goals[0], bird)

    def distance_next_pipe(self, bird: Bird) -> float:
        pipe = self.goals[0] if len(self.goals) != 0 else None
        return PipeController.distance_checkpoint(pipe, bird, self.real_height())

    def get_position(self, bird: Bird) -> str:
        pipe = self.goals[0] if len(self.goals) != 0 else None
        return PipeController.position_player_pipe(pipe, bird, self.real_height())

    def real_height(self):
        return self.board.height - self.texture_manager.texture["top"]["height"]

    def update(self) -> None:
        self.frequency -= 1
        for goal in self.goals:
            goal.position_x -= PIPE_SPEED

        if self.frequency == 0:
            pipe = PipeController.create_pipe(self.board.width, self.board.height)
            self.goals.append(pipe)
            self.frequency = PIPE_FREQUENCY

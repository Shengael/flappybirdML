from typing import List

from resources.env import PIPE_FREQUENCY
from resources.flappy_types import States
from src.entities.bird import Bird
from src.entities.board import Board
from src.controllers.pipe_controller import PipeController
from src.entities.pipe import Pipe


class BoardController:
    def __init__(self, width: int, height: int) -> None:
        self.board = Board(width, height)
        self.goals: List[Pipe] = []
        self.frequency = PIPE_FREQUENCY

    def is_bottom(self, bird: Bird) -> bool:
        return bird.get_bottom() <= 0

    def is_top(self, bird: Bird) -> bool:
        return bird.get_top() >= self.board.height - 1

    def is_pipe(self, bird: Bird) -> bool:
        return len(self.goals) != 0 and PipeController.in_pipe(self.goals[0], bird)

    def is_checkpoint(self, bird: Bird) -> bool:
        return len(self.goals) != 0 and PipeController.in_checkpoint(self.goals[0], bird)

    def distance_next_pipe(self, bird: Bird) -> float:
        if len(self.goals) == 0:
            return -1
        return PipeController.distance_checkpoint(self.goals[0], bird)

    def update(self) -> None:
        self.frequency -= 1
        self.board.states = {(y, x): self.board.states[(y, x + 1)] for y in range(self.board.height - 1) for x in
                             range(self.board.width)}

        for goal in self.goals:
            goal.position_x -= 1

        if self.frequency != 0:
            new_state = self.create_empty()
        else:
            pipe = PipeController.create_pipe(self.board.width, self.board.height)
            self.goals.append(pipe)
            new_state = pipe.state

        self.board.states = {**self.board.states, **new_state}

    def create_empty(self) -> States:
        return {(i, self.board.width - 1) for i in (1, self.board.height - 1)}

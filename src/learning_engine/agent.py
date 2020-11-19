import copy

from src.controllers.environment import Environment
from src.entities.bird import Bird
from src.learning_engine.policy import Policy


class Agent:

    def __init__(self, env: Environment, bird: Bird) -> None:
        self.environment = env
        self.previous_bird = bird
        self.score = 0
        self.reward = 0
        self.last_action = None
        self.policy = Policy(env.height - 1)

    def reset(self, bird: Bird) -> None:
        self.environment.reset()
        self.previous_bird = bird.reset()
        self.score = 0
        self.reward = 0

    def best_action(self, bird: Bird) -> str:
        return self.policy.best_action(bird.get_state(), self.environment.board_controller.get_position(bird))

    def do(self, bird: Bird, action: str) -> Bird:
        self.previous_bird = copy.deepcopy(bird)
        bird, self.reward = self.environment.update_bird(bird, action)
        self.score += self.reward
        self.last_action = action
        return bird

    def update_policy(self, bird: Bird) -> None:
        self.policy.update(self.previous_bird.get_state(), bird.get_state(),
                           self.environment.board_controller.get_position(self.previous_bird),
                           self.environment.board_controller.get_position(bird), self.last_action, self.reward)

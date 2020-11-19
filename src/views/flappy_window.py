import arcade

from resources.env import SPRITE_SIZE, GAP_SIZE
from src.controllers.texture_manager import TextureManager
from src.entities.bird import Bird
from src.learning_engine.agent import Agent


class FlappyWindow(arcade.Window):
    def __init__(self, agent: Agent, bird: Bird):
        super().__init__(agent.environment.width * SPRITE_SIZE,
                         agent.environment.height * SPRITE_SIZE,
                         "Flap Flap Flap")
        self.agent = agent
        self.bird = bird
        self.walls = None
        self.texture_manager = TextureManager()

    def setup(self):
        self.walls = arcade.SpriteList()
        environment = self.agent.environment
        self.texture_manager.create_pipe(environment.height, self.walls, environment.board_controller.goals)
        self.texture_manager.create_top(environment.width, environment.height, self.walls)
        self.texture_manager.create_bottom(environment.width, self.walls)

    def on_update(self, delta_time):
        action = self.agent.best_action(self.bird)
        self.setup()
        self.agent.environment.board_controller.update()
        self.bird = self.agent.do(self.bird, action)
        self.agent.update_policy(self.bird)
        if self.agent.environment.loose:
            if self.agent.environment.best_win_streak < self.agent.environment.win_streak:
                self.agent.environment.best_win_streak = self.agent.environment.win_streak
            self.agent.reset(self.bird)
        if self.agent.environment.checked:
            self.agent.score = 0

    def on_draw(self):
        arcade.start_render()

        self.walls.draw()
        self.bird.sprite.draw()

        arcade.draw_text(f"Win streak: {self.agent.environment.win_streak}", 10,
                         (self.agent.environment.height - 0.5) * self.bird.sprite.height - 10, arcade.csscolor.GREEN,
                         20)
        arcade.draw_text(f"best Win streak: {self.agent.environment.best_win_streak}", 300,
                         (self.agent.environment.height - 0.5) * self.bird.sprite.height - 10, arcade.csscolor.BLUE, 20)

        arcade.draw_text(f"Score: {self.agent.score}", 10, 10, arcade.csscolor.BLACK, 20)

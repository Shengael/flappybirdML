import arcade

from resources.env import SPRITE_SIZE, GAP_SIZE
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

    def setup(self):
        self.walls = arcade.SpriteList()
        self.create_pipe()
        self.create_top()
        self.create_bottom()

    def create_top(self):
        sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
        quantity = int(self.agent.environment.width / sprite.width) + 1

        for s in range(quantity):
            sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
            sprite.center_x = sprite.width * 0.5 + sprite.width * s
            sprite.center_y = self.agent.environment.height - (sprite.height * 0.5)
            self.walls.append(sprite)

    def create_bottom(self):
        sprite = arcade.Sprite(":resources:images/tiles/waterTop_high.png", 0.5)
        quantity = int(self.agent.environment.width / sprite.width) + 1

        for s in range(quantity):
            sprite = arcade.Sprite(":resources:images/tiles/waterTop_high.png", 0.5)
            sprite.center_x = sprite.width * 0.5 + sprite.width * s
            sprite.center_y = sprite.height * 0.5
            self.walls.append(sprite)

    def create_pipe(self):
        for pipe in self.agent.environment.board_controller.goals:
            sprite = arcade.Sprite(":resources:images/tiles/water.png", 0.5)
            quantity_top = int((self.agent.environment.height - pipe.top) / sprite.height) + 1
            quantity_bottom = int(pipe.bottom / sprite.height)

            for s in range(quantity_top):
                sprite = arcade.Sprite(":resources:images/tiles/water.png", 0.5)
                sprite.center_x = pipe.position_x + sprite.width * 0.5
                sprite.center_y = pipe.top + (sprite.height * 0.5 + sprite.height * s)
                self.walls.append(sprite)

            for s in range(quantity_bottom):
                sprite = arcade.Sprite(":resources:images/tiles/water.png", 0.5)
                sprite.center_x = pipe.position_x + sprite.width * 0.5
                sprite.center_y = pipe.bottom - (sprite.height * 0.5 + sprite.height * s)
                self.walls.append(sprite)

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

import arcade

from resources.env import SCREEN_WIDTH, SCREEN_HEIGHT
from src.controllers.environment import Environment
from src.entities.bird import Bird
from src.learning_engine.agent import Agent
from src.views.flappy_window import FlappyWindow

if __name__ == "__main__":
    environment = Environment(SCREEN_WIDTH, SCREEN_HEIGHT)
    bird = Bird()
    agent = Agent(environment, bird)

    window = FlappyWindow(agent, bird)
    window.setup()
    arcade.run()

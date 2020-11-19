import arcade

from src.controllers.environment import Environment
from src.entities.bird import Bird
from src.learning_engine.agent import Agent
from src.views.flappy_window import FlappyWindow

if __name__ == "__main__":
    environment = Environment(500, 800)
    bird = Bird()
    agent = Agent(environment, bird)

    window = FlappyWindow(agent, bird)
    window.setup()
    arcade.run()

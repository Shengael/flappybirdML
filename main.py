if __name__ == "__main__":
    # Initialiser l'environment
    environment = Environment(MAZE)

    # Initialiser l'agent
    agent = Agent(environment)

    # Lancer le jeu
    window = MazeWindow(agent)
    window.setup()
    arcade.run()
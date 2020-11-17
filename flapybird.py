import arcade
import random

UP, RELEASE = 'U', 'R'
ACTIONS = [UP, RELEASE]

MAZE = """
###########
           
 .         
           
           
           
           
           
           
           
           
___________
"""
REWARD_LOOSE = -9000
REWARD_IMPOSSIBLE = -60
REWARD_STUCK = -6
REWARD_DEFAULT = -1
# TODO: doit-il y avoir une fin ?
REWARD_CHECKPOINT = 15
REWARD_GOAL = 60
DEFAULT_LEARNING_RATE = 1
DEFAULT_DISCOUNT_FACTOR = 0.5
SPRITE_SIZE = 64
PIPE_FREQUENCY = 50
MIN_PIPE_SIZE = 1
GAP_SIZE = 2


class Environment:

    def __init__(self, text):
        self.goals = []
        self.initial = text
        self.reset()

    def reset(self):
        self.states = {}
        self.loose = False
        self.frequency = PIPE_FREQUENCY
        lines = self.initial.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])
        for row in range(self.height):
            for col in range(self.width):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] == '.':
                    self.starting_point = (row, col)
        return self.starting_point

    def check_pipe(self):
        self.frequency -= 1

        for row in range(self.height - 1):
            for col in range(self.width - 1):
                self.states[(row, col)] = self.states[(row, col + 1)]

        if self.frequency != 0:
            for i in range(1, self.height - 1):
                self.states[(i, self.width - 1)] = ' '
        else:
            self.frequency = PIPE_FREQUENCY
            top_pipe = random.randint(MIN_PIPE_SIZE + 1, self.height - 1 - MIN_PIPE_SIZE - GAP_SIZE)
            bottom_pipe = top_pipe + GAP_SIZE
            #self.goals.push({top: (x, y), bottom: (x, y)})

            self.states[(top_pipe, self.width - 1)] = '&'
            self.states[(bottom_pipe, self.width - 1)] = '&'
            for i in range(self.height - 1):
                if 1 <= i < top_pipe:
                    self.states[(i, self.width - 1)] = '@'
                elif bottom_pipe < i <= self.height:
                    self.states[(i, self.width - 1)] = '@'

    def apply(self, state, action):
        if action == UP:
            new_state = (state[0] - 1, state[1])
        elif action == RELEASE:
            new_state = (state[0] + 1, state[1])

        if new_state in self.states:
            # calculer la récompense
            if self.states[new_state] in ['#']:
                new_state = state
                reward = REWARD_STUCK
            elif self.states[new_state] in ['_', '@', '&']:  # Sortie du labyrinthe : grosse récompense
                self.loose = True
                reward = REWARD_LOOSE
            elif self.states[new_state] in ['+']:  # Sortie du labyrinthe : grosse récompense
                reward = REWARD_CHECKPOINT
            else:
                reward = REWARD_DEFAULT
        else:
            # Etat impossible: grosse pénalité
            new_state = state
            reward = REWARD_IMPOSSIBLE

        return new_state, reward


class Agent:

    def __init__(self, env):
        self.environment = env
        self.policy = Policy(env.states.keys(), ACTIONS)
        self.reset()

    def reset(self):
        self.state = self.environment.reset()
        self.previous_state = self.state
        self.score = 0

    def best_action(self):
        return self.policy.best_action(self.state)

    def do(self, action):
        self.previous_state = self.state
        #
        self.state, self.reward = self.environment.apply(self.state, action)
        self.score += self.reward
        self.last_action = action

    def update_policy(self):
        self.policy.update(self.previous_state, self.state, self.last_action, self.reward)


class Policy:  # Q-table
    def __init__(self, states, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        for s in states:
            self.table[s] = {}
            for a in actions:
                self.table[s][a] = 0

    def __repr__(self):
        res = ''
        for state in self.table:
            res += f'{state}\t{self.table[state]}\n'
        return res

    def best_action(self, state):
        action = None
        for a in self.table[state]:
            if action is None or self.table[state][a] > self.table[state][action]:
                action = a
        return action

    def update(self, previous_state, state, last_action, reward):
        # Q(st, at) = Q(st, at) + learning_rate * (reward + discount_factor * max(Q(state)) - Q(st, at))
        maxQ = max(self.table[state].values())
        self.table[previous_state][last_action] += self.learning_rate * \
                                                   (reward + self.discount_factor * maxQ - self.table[previous_state][
                                                       last_action])


class MazeWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(agent.environment.width * SPRITE_SIZE,
                         agent.environment.height * SPRITE_SIZE,
                         "Escape from ESGI")
        self.agent = agent

    def setup(self):
        self.walls = arcade.SpriteList()

        for state in agent.environment.states:
            if agent.environment.states[state] == '#':
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)
            if agent.environment.states[state] == '@':
                sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)
            if agent.environment.states[state] == '&':
                sprite = arcade.Sprite(":resources:images/tiles/stoneCenter_rounded.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)
            if agent.environment.states[state] == '_':
                sprite = arcade.Sprite(":resources:images/tiles/waterTop_high.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)

        self.player = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png",
                                    0.5)
        self.update_player_xy()

    def update_player_xy(self):
        self.player.center_x = self.player.height * (self.agent.state[1] + 0.5)
        self.player.center_y = self.player.height * (agent.environment.height - self.agent.state[0] - 0.5)

    def on_update(self, delta_time):
        action = self.agent.best_action()
        self.setup()
        self.agent.environment.check_pipe()
        self.agent.do(action)
        self.agent.update_policy()
        self.update_player_xy()
        if self.agent.environment.loose:
            print('loose')
            self.agent.reset()

    def on_draw(self):
        arcade.start_render()

        self.walls.draw()
        self.player.draw()

        arcade.draw_text(f"Score: {self.agent.score}", 10, 10, arcade.csscolor.BLACK, 20)


if __name__ == "__main__":
    # Initialiser l'environment
    environment = Environment(MAZE)

    # Initialiser l'agent
    agent = Agent(environment)

    # Lancer le jeu
    window = MazeWindow(agent)
    window.setup()
    arcade.run()

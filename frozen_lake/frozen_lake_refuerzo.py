import numpy as np
import random
import matplotlib.pyplot as plt

class FrozenLake:
    def __init__(self, size=4):
        self.size = size
        self.state = (0, 0)  # Posición inicial
        self.goal = (size - 1, size - 1)  # Meta
        self.holes = self.place_holes(3)  # Colocar agujeros
        self.state_space = size * size  # Espacio de estados
        self.action_space = 4  # 0: arriba, 1: abajo, 2: izquierda, 3: derecha

    def place_holes(self, n):
        holes = set()
        while len(holes) < n:
            hole = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if hole != self.goal and hole != (0, 0):
                holes.add(hole)
        return holes

    def reset(self):
        self.state = (0, 0)
        return self.state

    def step(self, action):
        x, y = self.state
        
        # Moverse según la acción
        if action == 0 and x > 0:  # Arriba
            x -= 1
        elif action == 1 and x < self.size - 1:  # Abajo
            x += 1
        elif action == 2 and y > 0:  # Izquierda
            y -= 1
        elif action == 3 and y < self.size - 1:  # Derecha
            y += 1

        self.state = (x, y)
        reward = -1  # Penalización por cada paso
        done = False

        if self.state in self.holes:  # Si cae en un agujero
            reward = -10
            done = True
        elif self.state == self.goal:  # Si llega a la meta
            reward = 10
            done = True

        return self.state, reward, done

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.env = env
        self.q_table = np.zeros((env.state_space, env.action_space))  # Inicializar la tabla Q
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = 0.99
        self.exploration_min = 0.01

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:  # Exploración
            return random.randint(0, self.env.action_space - 1)
        else:  # Explotación
            return np.argmax(self.q_table[state[0] * self.env.size + state[1]])

    def update_q_table(self, state, action, reward, next_state):
        state_index = state[0] * self.env.size + state[1]
        next_state_index = next_state[0] * self.env.size + next_state[1]
        best_next_action = np.argmax(self.q_table[next_state_index])
        td_target = reward + self.discount_factor * self.q_table[next_state_index][best_next_action]
        td_delta = td_target - self.q_table[state_index][action]
        self.q_table[state_index][action] += self.learning_rate * td_delta

    def train(self, episodes):
        wins = []
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            done = False
            win = False

            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update_q_table(state, action, reward, next_state)

                total_reward += reward
                state = next_state

                if reward == 10:  # Si gana
                    win = True

            if win:
                wins.append(1)
                print(f"Episodio {episode + 1}: Ganó")
            else:
                wins.append(0)
                print(f"Episodio {episode + 1}: Perdió")

            # Decay exploration rate
            self.exploration_rate = max(self.exploration_min, self.exploration_rate * self.exploration_decay)

        return wins

def plot_wins(wins):
    plt.plot(np.cumsum(wins))  # Sumar el número de victorias acumuladas
    plt.title('Victorias acumuladas en el tiempo')
    plt.xlabel('Episodios')
    plt.ylabel('Victorias acumuladas')
    plt.show()

if __name__ == "__main__":
    env = FrozenLake()
    agent = QLearningAgent(env)
    episodes = 1000
    wins = agent.train(episodes)
    plot_wins(wins)

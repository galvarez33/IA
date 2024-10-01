import numpy as np
import random
import matplotlib.pyplot as plt

# Clase que representa el entorno de Blackjack
class Blackjack:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.state = None

    def create_deck(self):
        # Crea un mazo de cartas
        return [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

    def reset(self):
        # Reinicia el juego y crea un nuevo mazo
        self.deck = self.create_deck()  # Asegúrate de reiniciar el mazo aquí
        random.shuffle(self.deck)
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]
        self.state = (self.player_hand_value(), self.dealer_hand[0])
        return self.state

    def draw_card(self):
        # Roba una carta del mazo
        return self.deck.pop()

    def player_hand_value(self):
        # Calcula el valor de la mano del jugador
        value = sum(self.player_hand)
        # Ajusta el valor si hay ases
        while value > 21 and 11 in self.player_hand:
            self.player_hand.remove(11)
            self.player_hand.append(1)
            value = sum(self.player_hand)
        return value

    def step(self, action):
        if action == 1:  # Hit
            self.player_hand.append(self.draw_card())
            player_value = self.player_hand_value()
            if player_value > 21:
                return self.state, -1, True  # El jugador pierde
        else:  # Stand
            dealer_value = self.dealer_hand_value()
            while dealer_value < 17:
                self.dealer_hand.append(self.draw_card())
                dealer_value = self.dealer_hand_value()

            player_value = self.player_hand_value()
            if dealer_value > 21 or player_value > dealer_value:
                return self.state, 1, True  # El jugador gana
            elif player_value < dealer_value:
                return self.state, -1, True  # El jugador pierde
            else:
                return self.state, 0, True  # Empate

        self.state = (self.player_hand_value(), self.dealer_hand[0])
        return self.state, 0, False  # Juego continúa

    def dealer_hand_value(self):
        # Calcula el valor de la mano del dealer
        value = sum(self.dealer_hand)
        while value > 21 and 11 in self.dealer_hand:
            self.dealer_hand.remove(11)
            self.dealer_hand.append(1)
            value = sum(self.dealer_hand)
        return value

# Clase del agente que utiliza Q-learning
class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    def get_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice([0, 1])  # 0: Stand, 1: Hit
        return np.argmax(self.q_table.get(state, [0, 0]))

    def update(self, state, action, reward, next_state):
        old_value = self.q_table.get(state, [0, 0])[action]
        future_reward = max(self.q_table.get(next_state, [0, 0]), default=0)
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * future_reward)

        if state not in self.q_table:
            self.q_table[state] = [0, 0]
        self.q_table[state][action] = new_value

# Main Loop
if __name__ == "__main__":
    env = Blackjack()
    agent = QLearningAgent()
    episodes = 10000
    rewards = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = agent.get_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state)
            state = next_state
            total_reward += reward

        rewards.append(total_reward)

        # Imprimir progreso de aprendizaje en español
        if episode % 1000 == 0:
            porcentaje = (episode / episodes) * 100
            print(f"Episodio: {episode}, Recompensa Total: {total_reward}, Tamaño de la tabla Q: {len(agent.q_table)}, Progreso de aprendizaje: {porcentaje:.2f}%")

    # Visualizar el rendimiento
    plt.plot(rewards)
    plt.title('Recompensas Totales por Episodio')
    plt.xlabel('Episodios')
    plt.ylabel('Recompensa Total')
    plt.show()

    # Simulación de una partida final
    print("\nSimulación de una partida final:")
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.get_action(state)  # Usa la política aprendida
        next_state, reward, done = env.step(action)
        state = next_state
        total_reward += reward

        # Mostrar cartas del jugador y del dealer
        print(f"\nMano del Jugador: {env.player_hand} (Valor: {env.player_hand_value()})")
        print(f"Mano del Dealer: {env.dealer_hand} (Valor: {env.dealer_hand_value()})")
        print("Acción tomada:", "Pedir carta" if action == 1 else "Plantarse")

    # Resultado de la partida
    if total_reward == 1:
        print("\n¡El jugador gana la partida!")
    elif total_reward == -1:
        print("\nEl jugador pierde la partida.")
    else:
        print("\nLa partida terminó en empate.")

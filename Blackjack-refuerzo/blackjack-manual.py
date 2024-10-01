import numpy as np
import random

class Blackjack:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False

    def deal_card(self):
        return random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10])  # Asumimos que 10 representa las figuras

    def calculate_hand(self, hand):
        return sum(hand)

    def player_turn(self):
        while True:
            action = input("¿Quieres pedir (p) o plantarte (s)? ")
            if action == 'p':
                self.player_hand.append(self.deal_card())
                print(f"Tu mano: {self.player_hand}, total: {self.calculate_hand(self.player_hand)}")
                if self.calculate_hand(self.player_hand) > 21:
                    print("Te pasaste. Pierdes.")
                    self.game_over = True
                    break
            elif action == 's':
                break

    def dealer_turn(self):
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())

    def play_game(self):
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card()]
        print(f"Mano del crupier: {self.dealer_hand[0]} y una carta oculta.")

        self.player_turn()
        if not self.game_over:
            self.dealer_turn()
            player_total = self.calculate_hand(self.player_hand)
            dealer_total = self.calculate_hand(self.dealer_hand)
            print(f"Tu mano: {self.player_hand}, total: {player_total}")
            print(f"Mano del crupier: {self.dealer_hand}, total: {dealer_total}")

            if dealer_total > 21 or player_total > dealer_total:
                print("¡Ganaste!")
            elif player_total < dealer_total:
                print("Perdiste.")
            else:
                print("Es un empate.")

if __name__ == "__main__":
    game = Blackjack()
    game.play_game()

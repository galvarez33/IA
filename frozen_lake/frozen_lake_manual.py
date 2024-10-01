import random
import tkinter as tk
from tkinter import messagebox

class FrozenLakeGame:
    def __init__(self, master):
        self.master = master
        self.size = 4
        self.board = self.create_board()
        self.player_pos = (0, 0)  # Start at the top-left corner
        self.goal_pos = (self.size - 1, self.size - 1)  # Goal at bottom-right corner
        self.holes = self.place_holes(3)  # Place 3 holes randomly

        # Set up the GUI
        self.canvas = tk.Canvas(master, width=300, height=300)
        self.canvas.pack()

        self.draw_board()
        self.master.bind('<Key>', self.move)

    def create_board(self):
        return [['F' for _ in range(self.size)] for _ in range(self.size)]

    def place_holes(self, count):
        holes = set()
        while len(holes) < count:
            hole = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if hole != self.player_pos and hole != self.goal_pos:  # Don't place on player or goal
                holes.add(hole)

        for hole in holes:
            self.board[hole[0]][hole[1]] = 'H'  # Mark holes on the board
        return holes

    def draw_board(self):
        self.canvas.delete("all")  # Clear the canvas
        cell_size = 75  # Size of each cell in the grid

        for r in range(self.size):
            for c in range(self.size):
                x0 = c * cell_size
                y0 = r * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size

                if (r, c) == self.player_pos:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='blue')  # Player
                elif (r, c) == self.goal_pos:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='green')  # Goal
                elif (r, c) in self.holes:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='red')  # Hole
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')  # Free space

                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=self.board[r][c])

    def move(self, event):
        x, y = self.player_pos
        if event.keysym == 'Up':  # Move up
            x = max(x - 1, 0)
        elif event.keysym == 'Down':  # Move down
            x = min(x + 1, self.size - 1)
        elif event.keysym == 'Left':  # Move left
            y = max(y - 1, 0)
        elif event.keysym == 'Right':  # Move right
            y = min(y + 1, self.size - 1)

        self.player_pos = (x, y)
        self.check_state()
        self.draw_board()

    def check_state(self):
        if self.player_pos in self.holes:
            messagebox.showinfo("Fin del juego", "¡Has caído en un agujero!")
            self.reset_game()
        elif self.player_pos == self.goal_pos:
            messagebox.showinfo("Fin del juego", "¡Felicidades! Has llegado al objetivo!")
            self.reset_game()

    def reset_game(self):
        self.board = self.create_board()
        self.player_pos = (0, 0)
        self.goal_pos = (self.size - 1, self.size - 1)
        self.holes = self.place_holes(3)
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Frozen Lake")
    game = FrozenLakeGame(root)
    root.mainloop()

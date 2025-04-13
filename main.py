import tkinter as tk
from tkinter import messagebox
import random

class Game:
    def __init__(self, window):
        self.window = window
        self.window.title("Tic Tac Toe")
        self.window.geometry("400x500")

        self.name_x = "Player X"
        self.name_o = "Player O"
        self.turn = "X"
        self.cells = ["" for _ in range(9)]
        self.tiles = []
        self.vs_computer = False

        self.info_label = tk.Label(self.window, text="", font=('Helvetica', 18))
        self.info_label.pack(pady=20)

        self.board_frame = tk.Frame(self.window)
        self.board_frame.pack()

        self.setup_board()
        self.hide_board()

    def setup_board(self):
        for i in range(9):
            tile = tk.Button(self.board_frame, text="", font=('Helvetica', 32), width=4, height=2,
                             command=lambda i=i: self.select_tile(i))
            tile.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.tiles.append(tile)

    def hide_board(self):
        self.board_frame.pack_forget()
        self.info_label.config(text="")

    def show_board(self):
        self.board_frame.pack()
        self.update_info_label()

    def select_tile(self, index):
        if self.cells[index] == "" and not self.find_winner():
            self.cells[index] = self.turn
            self.tiles[index].config(text=self.turn)
            winner = self.find_winner()
            if winner:
                winner_name = self.name_x if winner == "X" else self.name_o
                messagebox.showinfo("Game Over", f"{winner_name} wins!")
                self.offer_restart()
            elif "" not in self.cells:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.offer_restart()
            else:
                self.turn = "O" if self.turn == "X" else "X"
                self.update_info_label()
                if self.vs_computer and self.turn == "O":
                    self.window.after(500, self.computer_move)

    def computer_move(self):
        # Improved strategy: win if possible, block if necessary, else random
        for i in range(9):
            if self.cells[i] == "":
                self.cells[i] = "O"
                if self.find_winner() == "O":
                    self.cells[i] = ""
                    self.select_tile(i)
                    return
                self.cells[i] = ""

        for i in range(9):
            if self.cells[i] == "":
                self.cells[i] = "X"
                if self.find_winner() == "X":
                    self.cells[i] = ""
                    self.select_tile(i)
                    return
                self.cells[i] = ""

        empty_indices = [i for i, val in enumerate(self.cells) if val == ""]
        if empty_indices:
            index = random.choice(empty_indices)
            self.select_tile(index)

    def update_info_label(self):
        current_name = self.name_x if self.turn == "X" else self.name_o
        self.info_label.config(text=f"{current_name}'s Turn ({self.turn})")

    def find_winner(self):
        win_combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in win_combos:
            if self.cells[a] == self.cells[b] == self.cells[c] != "":
                return self.cells[a]
        return None

    def offer_restart(self):
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            self.restart_game()
        else:
            self.window.quit()

    def restart_game(self):
        self.cells = ["" for _ in range(9)]
        self.turn = "X"
        self.update_info_label()
        for tile in self.tiles:
            tile.config(text="")

if __name__ == "__main__":
    def ask_names():
        name_window = tk.Tk()
        name_window.title("Start New Game")
        name_window.geometry("400x300")

        def start_game():
            name_x = entry_x.get() or "Player X"
            opponent = var.get()
            name_o = entry_o.get() or "Player O" if opponent == "human" else "Computer"

            name_window.destroy()

            root = tk.Tk()
            game = Game(root)
            game.name_x = name_x
            game.name_o = name_o
            game.vs_computer = (opponent == "computer")
            game.show_board()

            if game.vs_computer and game.turn == "O":
                root.after(500, game.computer_move)

            root.mainloop()

        tk.Label(name_window, text="Player X Name:").pack(pady=5)
        entry_x = tk.Entry(name_window)
        entry_x.pack(pady=5)

        var = tk.StringVar(value="human")
        tk.Radiobutton(name_window, text="Play against Human", variable=var, value="human").pack()
        tk.Radiobutton(name_window, text="Play against Computer", variable=var, value="computer").pack()

        tk.Label(name_window, text="Player O Name (if human):").pack(pady=5)
        entry_o = tk.Entry(name_window)
        entry_o.pack(pady=5)

        tk.Button(name_window, text="Start Game", command=start_game).pack(pady=10)

        name_window.mainloop()

    ask_names()
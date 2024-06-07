import random
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# File to store high scores
HIGH_SCORES_FILE = "high_scores.json"

def load_high_scores():
    try:
        with open(HIGH_SCORES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_high_scores(high_scores):
    with open(HIGH_SCORES_FILE, "w") as file:
        json.dump(high_scores, file)

def update_high_score(name, score, high_scores):
    if name in high_scores:
        if score < high_scores[name]:
            high_scores[name] = score
    else:
        high_scores[name] = score
    save_high_scores(high_scores)

class GuessTheNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("U Guess It")

        self.name = tk.StringVar()
        self.guess = tk.IntVar()
        self.message = tk.StringVar()
        self.attempts = 0
        self.max_attempts = 0
        self.number_to_guess = 0
        self.last_guess = None
        self.high_scores = load_high_scores()

        self.setup_widgets()

    def setup_widgets(self):
        self.root.configure(bg='#f7d794')  # Light yellow background

        title_label = tk.Label(self.root, text="U Guess It", font=("Helvetica", 28, "bold"), fg="#ff6b6b", bg='#f7d794')
        title_label.pack(pady=20)

        credits_label = tk.Label(self.root, text="Maded By S.Stefanov", font=("Helvetica", 10, "italic"), fg="#ff6b6b", bg='#f7d794')
        credits_label.pack(side=tk.BOTTOM, pady=10)

        self.message_label = tk.Label(self.root, textvariable=self.message, font=("Helvetica", 14), fg="#4b7bec", bg='#f7d794')
        self.message_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.root, textvariable=self.guess, font=("Helvetica", 14), bg="#fffa65", fg="#303952")
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", self.check_guess)

        self.guess_button = tk.Button(self.root, text="Guess", font=("Helvetica", 14), command=self.check_guess, bg="#32ff7e", fg="#ffffff", activebackground="#3ae374")
        self.guess_button.pack(pady=20)
        self.guess_button.config(state=tk.DISABLED)  # Disable until game starts

        self.start_game()

    def start_game(self):
        self.name.set(simpledialog.askstring("Name", "Enter your name:", parent=self.root))
        self.message.set(f"Hello {self.name.get()}, let's start the game!")
        self.choose_difficulty()

    def choose_difficulty(self):
        level = simpledialog.askstring("Difficulty", "Choose a difficulty level:\n1. Easy (1-10, 10 attempts)\n2. Medium (1-50, 7 attempts)\n3. Hard (1-100, 5 attempts)", parent=self.root)
        if level == '1':
            self.max_attempts = 10
            self.number_to_guess = random.randint(1, 10)
        elif level == '2':
            self.max_attempts = 7
            self.number_to_guess = random.randint(1, 50)
        elif level == '3':
            self.max_attempts = 5
            self.number_to_guess = random.randint(1, 100)
        else:
            messagebox.showerror("Invalid choice", "Please enter 1, 2, or 3.")
            self.choose_difficulty()
            return
        self.message.set(f"Great, you chose level {level}. You have {self.max_attempts} attempts to guess the number.")
        self.guess_button.config(state=tk.NORMAL)

    def check_guess(self, event=None):
        try:
            guess = self.guess.get()
            self.attempts += 1

            if self.last_guess is not None:
                if abs(guess - self.number_to_guess) < abs(self.last_guess - self.number_to_guess):
                    self.message.set("Warmer!")
                else:
                    self.message.set("Colder!")

            if guess < self.number_to_guess:
                self.message.set("Too low! Try again.")
            elif guess > self.number_to_guess:
                self.message.set("Too high! Try again.")
            else:
                self.message.set(f"Congratulations, {self.name.get()}! You've guessed the number in {self.attempts} attempts.")
                update_high_score(self.name.get(), self.attempts, self.high_scores)
                self.show_high_scores()
                self.guess_button.config(state=tk.DISABLED)
                return

            self.last_guess = guess

            if self.attempts >= self.max_attempts:
                self.message.set(f"Sorry, {self.name.get()}. You've used all {self.max_attempts} attempts. The number was {self.number_to_guess}.")
                self.show_high_scores()
                self.guess_button.config(state=tk.DISABLED)

        except ValueError:
            self.message.set("Please enter a valid number.")

    def show_high_scores(self):
        scores = "\n".join([f"{player}: {score} attempts" for player, score in self.high_scores.items()])
        messagebox.showinfo("High Scores", scores)

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheNumberGame(root)
    root.mainloop()

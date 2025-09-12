import random

class WordGuessGame:
    def __init__(self):
        self.words = ["Impossible", "Binary", "Palestine", "Auckland", "Artificial", "Intelligence"]
        self.word = random.choice(self.words).lower()  # store as lowercase for easy matching
        self.blanks = ["_"] * len(self.word)
        self.lives = 6

    def get_guess(self):
        return input("Guess a letter: ").lower()

    def update_blanks(self, guess):
        correct = False
        for i, letter in enumerate(self.word):
            if letter == guess and self.blanks[i] == "_":
                self.blanks[i] = guess
                correct = True
        return correct

    def play(self):
        print("Welcome to the Word Guessing Game!")
        print("You have", self.lives, "lives.")
        print(" ".join(self.blanks))

        while self.lives > 0:
            guess = self.get_guess()

            if self.update_blanks(guess):
                print("Good guess!")
            else:
                self.lives -= 1
                print("Wrong guess! Lives left:", self.lives)

            print(" ".join(self.blanks))

            if "_" not in self.blanks:
                print("🎉 Congratulations! You guessed the word:", self.word)
                break
        else:
            print("💀 Game over! The word was:", self.word)

# Run the game
if __name__ == "__main__":
    game = WordGuessGame()
    game.play()
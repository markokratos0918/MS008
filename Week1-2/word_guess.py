import random

# 1. Generate a random word
def choose_word():
    words = ["Impossible", "Binary", "Palestine", "Auckland", "Artificial", "Intelligence"]
    return random.choice(words)

# 2. Generate blanks for the chosen word
def create_blanks(word):
    return ["_"] * len(word)

# 3. Ask the user for a guess
def get_guess():
    return input("Guess a letter: ").lower()

# 4. Update the blanks if guess is correct
def update_blanks(word, blanks, guess):
    correct = False
    for i, letter in enumerate(word):
        if letter == guess and blanks[i] == "_":
            blanks[i] = guess
            correct = True
    return correct

# 5–9. Game loop
def play_game():
    word = choose_word()
    blanks = create_blanks(word)
    lives = 6  # You can adjust number of lives

    print("Welcome to the Word Guessing Game!")
    print("You have", lives, "lives.")
    print(" ".join(blanks))

    while lives > 0:
        guess = get_guess()

        if update_blanks(word, blanks, guess):
            print("Good guess!")
        else:
            lives -= 1
            print("Wrong guess! Lives left:", lives)

        print(" ".join(blanks))

        # Win condition
        if "_" not in blanks:
            print("🎉 Congratulations! You guessed the word:", word)
            break
    else:
        print("💀 Game over! The word was:", word)

# Run the game
if __name__ == "__main__":
    play_game()

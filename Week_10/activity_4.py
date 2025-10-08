"""
Tic-Tac-Toe Game Implementation with Timer and Symbol Selection.

A complete implementation of Tic-Tac-Toe game using Object-Oriented Programming.
Features: Two players, symbol selection, 10-second turn timer, move validation.
"""

import time
import threading
import sys


class Board:
    """Represents the Tic-Tac-Toe game board."""

    def __init__(self):
        """Initialize a 3x3 empty board."""
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
        self.size = 3

    def display(self):
        """Display the current state of the board."""
        print("\n" + "=" * 13)
        for i, row in enumerate(self.grid):
            print(f" {row[0]} | {row[1]} | {row[2]} ")
            if i < self.size - 1:
                print("-----------")
        print("=" * 13 + "\n")

    def is_valid_move(self, row, col):
        """
        Check if a move is valid.

        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)

        Returns:
            bool: True if move is valid, False otherwise
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        return self.grid[row][col] == ' '

    def make_move(self, row, col, symbol):
        """
        Place a symbol on the board.

        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            symbol (str): Player symbol ('X' or 'O')

        Returns:
            bool: True if move was successful, False otherwise
        """
        if self.is_valid_move(row, col):
            self.grid[row][col] = symbol
            return True
        return False

    def is_full(self):
        """
        Check if the board is full.

        Returns:
            bool: True if board is full, False otherwise
        """
        return all(cell != ' ' for row in self.grid for cell in row)

    def check_winner(self):
        """
        Check if there's a winner on the board.

        Returns:
            str: Winning symbol ('X' or 'O') or None if no winner
        """
        # Check rows
        for row in self.grid:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        # Check columns
        for col in range(self.size):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != ' ':
                return self.grid[0][col]

        # Check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ' ':
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ' ':
            return self.grid[0][2]

        return None

    def reset(self):
        """Reset the board to empty state."""
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]


class Player:
    """Represents a player in the game."""

    def __init__(self, name, symbol):
        """
        Initialize a player.

        Args:
            name (str): Player's name
            symbol (str): Player's symbol ('X' or 'O')
        """
        self.name = name
        self.symbol = symbol
        self.wins = 0
        self.timeouts = 0

    def __str__(self):
        """
        Return string representation of player.

        Returns:
            str: Player information
        """
        return f"{self.name} ({self.symbol})"


class Timer:
    """Handles turn timer functionality."""

    def __init__(self, duration=10):
        """
        Initialize timer.

        Args:
            duration (int): Timer duration in seconds (default: 10)
        """
        self.duration = duration
        self.time_left = duration
        self.is_running = False
        self.timer_thread = None
        self.timeout_occurred = False

    def start(self):
        """Start the countdown timer."""
        self.time_left = self.duration
        self.is_running = True
        self.timeout_occurred = False
        self.timer_thread = threading.Thread(target=self._countdown, daemon=True)
        self.timer_thread.start()

    def stop(self):
        """Stop the countdown timer."""
        self.is_running = False
        if self.timer_thread:
            self.timer_thread.join(timeout=0.1)

    def _countdown(self):
        """Internal countdown logic."""
        while self.time_left > 0 and self.is_running:
            time.sleep(1)
            if self.is_running:
                self.time_left -= 1
                if self.time_left <= 5 and self.time_left > 0:
                    print(f"\r⏰ {self.time_left} seconds left...", end='', flush=True)
                    sys.stdout.flush()

        if self.is_running and self.time_left == 0:
            self.timeout_occurred = True
            print("\n\n⏱️  TIME'S UP! Turn skipped.\n")

    def has_timed_out(self):
        """
        Check if timer has expired.

        Returns:
            bool: True if timeout occurred
        """
        return self.timeout_occurred


class TicTacToe:
    """Main game controller for Tic-Tac-Toe."""

    def __init__(self, timer_duration=10):
        """
        Initialize the game.

        Args:
            timer_duration (int): Seconds per turn (default: 10)
        """
        self.board = Board()
        self.players = []
        self.current_player_index = 0
        self.game_over = False
        self.timer = Timer(timer_duration)

    def setup_players(self):
        """Set up the two players for the game."""
        print("=" * 40)
        print("   TIC-TAC-TOE GAME WITH TIMER")
        print("=" * 40)

        name1 = input("\nEnter Player 1 name: ").strip() or "Player 1"

        # Player 1 chooses symbol
        while True:
            choice = input(f"\n{name1}, choose your symbol (X/O): ").strip().upper()
            if choice in ['X', 'O']:
                symbol1 = choice
                symbol2 = 'O' if symbol1 == 'X' else 'X'
                break
            print("❌ Invalid choice! Please enter X or O.")

        name2 = input(f"\nEnter Player 2 name: ").strip() or "Player 2"

        self.players.append(Player(name1, symbol1))
        self.players.append(Player(name2, symbol2))

        print(f"\n✅ {self.players[0]} vs {self.players[1]}")
        print(f"⏱️  Each turn has a {self.timer.duration}-second limit!")
        print(f"🎮 {self.players[0].name} goes first!\n")

    def get_current_player(self):
        """
        Get the current player.

        Returns:
            Player: Current player object
        """
        return self.players[self.current_player_index]

    def switch_player(self):
        """Switch to the next player."""
        self.current_player_index = 1 - self.current_player_index

    def get_player_move(self):
        """
        Get and validate player move input with timer.

        Returns:
            tuple: (row, col) coordinates, None if invalid, or 'timeout'/'quit'
        """
        current_player = self.get_current_player()
        print(f"{current_player.name}'s turn ({current_player.symbol})")
        print(f"⏱️  You have {self.timer.duration} seconds to move!")

        # Start timer
        self.timer.start()

        move_input = None
        try:
            # Use a thread to handle input with timeout awareness
            move_input = input("Enter your move (row col) [1-3 1-3]: ").strip()

            # Stop timer immediately after input
            self.timer.stop()

            # Check if timeout occurred during input
            if self.timer.has_timed_out():
                return 'timeout'

            if move_input.lower() in ['quit', 'exit', 'q']:
                return 'quit'

            parts = move_input.split()
            if len(parts) != 2:
                print("❌ Invalid input! Please enter two numbers separated by space.")
                return None

            row = int(parts[0]) - 1
            col = int(parts[1]) - 1

            if not (0 <= row < 3 and 0 <= col < 3):
                print("❌ Invalid position! Use numbers 1-3 for both row and column.")
                return None

            return (row, col)

        except ValueError:
            self.timer.stop()
            print("❌ Invalid input! Please enter numbers only.")
            return None
        except (KeyboardInterrupt, EOFError):
            self.timer.stop()
            return 'quit'

    def play_turn(self):
        """
        Execute a single turn of the game.

        Returns:
            str: 'quit', 'timeout', or None for normal play
        """
        self.board.display()

        while True:
            move = self.get_player_move()

            if move == 'quit':
                return 'quit'

            if move == 'timeout':
                current_player = self.get_current_player()
                current_player.timeouts += 1
                print(f"⏱️  {current_player.name} ran out of time! Turn skipped.\n")
                return 'timeout'

            if move is None:
                continue

            row, col = move

            if self.board.make_move(row, col, self.get_current_player().symbol):
                print(f"✅ Move placed at ({row + 1}, {col + 1})")
                break

            print("❌ That position is already taken! Choose another.")

        return None

    def check_game_status(self):
        """
        Check if game is over (winner or draw).

        Returns:
            bool: True if game is over, False otherwise
        """
        winner = self.board.check_winner()

        if winner:
            self.board.display()
            current_player = self.get_current_player()
            print("=" * 40)
            print(f"🎉 {current_player.name} WINS! 🎉")
            print("=" * 40)
            current_player.wins += 1
            self.game_over = True
            return True

        if self.board.is_full():
            self.board.display()
            print("=" * 40)
            print("🤝 It's a DRAW! 🤝")
            print("=" * 40)
            self.game_over = True
            return True

        return False

    def play_game(self):
        """Run the main game loop."""
        self.setup_players()

        while not self.game_over:
            result = self.play_turn()

            if result == 'quit':
                print("\n👋 Game ended by player.")
                break

            if result == 'timeout':
                # Skip turn, check if board is full
                if self.board.is_full():
                    self.board.display()
                    print("=" * 40)
                    print("🤝 It's a DRAW! 🤝")
                    print("=" * 40)
                    self.game_over = True
                    break

            if self.check_game_status():
                break

            self.switch_player()

    def play_again(self):
        """
        Ask if players want to play again.

        Returns:
            bool: True if players want to play again
        """
        while True:
            choice = input("\nPlay again? (yes/no): ").strip().lower()
            if choice in ['yes', 'y']:
                return True
            if choice in ['no', 'n']:
                return False
            print("Please enter 'yes' or 'no'")

    def show_statistics(self):
        """Display game statistics."""
        print("\n" + "=" * 40)
        print("   GAME STATISTICS")
        print("=" * 40)
        for player in self.players:
            print(f"{player.name}: {player.wins} wins, {player.timeouts} timeouts")
        print("=" * 40)

    def run(self):
        """Run the complete game with replay option."""
        while True:
            self.board.reset()
            self.game_over = False
            self.current_player_index = 0

            self.play_game()

            if not self.play_again():
                self.show_statistics()
                print("\n👋 Thanks for playing! Goodbye!\n")
                break


def main():
    """Main entry point for the game."""
    game = TicTacToe(timer_duration=10)
    game.run()


if __name__ == "__main__":
    main()
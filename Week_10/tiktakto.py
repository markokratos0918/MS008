def print_board(board):
    print("\n")
    for i in range(3):
        row = "|".join(board[i])
        print(" " + row)
        if i < 2:
            print("---+---+---")
    print("\n")

def check_winner(board, player):
    # Check rows, columns and diagonals
    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def is_full(board):
    return all([cell != " " for row in board for cell in row])

def play():
    board = [[" "] * 3 for _ in range(3)]
    current_player = "X"
    while True:
        print_board(board)
        # Get move
        move = input(f"Player {current_player}, enter row and col (1-3, separated by space): ")
        try:
            row, col = map(int, move.strip().split())
            row -= 1
            col -= 1
            if board[row][col] != " ":
                print("Cell already taken, try again.")
                continue
            board[row][col] = current_player
        except (ValueError, IndexError):
            print("Invalid input, try again.")
            continue
        # Check winner
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        # Check draw
        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play()

import random

def print_board(board):
    """Prints the current state of the board."""
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("---------")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("---------")
    print(f"{board[6]} | {board[7]} | {board[8]}")

def check_winner(board, player):
    """Checks if the given player has won."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return ' ' not in board

def get_player_move(board):
    """Gets a valid move from the player using zero-based indexing internally."""
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if 0 <= move < 9 and board[move] == ' ':
                return move
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")

def get_computer_move(board):
    """Gets a random valid move for the computer."""
    available_moves = [i for i, x in enumerate(board) if x == ' ']
    return random.choice(available_moves)

def main():
    board = [' '] * 9
    current_player = random.choice(['X', 'O'])  # Randomly choose starting player
    
    while True:
        print_board(board)
        print(f"Current player: {current_player}")
        
        if current_player == 'X':
            move = get_player_move(board)
        else:
            move = get_computer_move(board)
        
        board[move] = current_player
        print(f"Move made by {current_player} at position {move + 1}")
        
        # Debug print to check player switching
        print(f"Switching from {current_player} to {'O' if current_player == 'X' else 'X'}")
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'

if __name__ == "__main__":
    main()

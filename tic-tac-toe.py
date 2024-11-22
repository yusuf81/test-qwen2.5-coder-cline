import random
import sys

# Constants for board positions
TOP_LEFT = 0
TOP_CENTER = 1
TOP_RIGHT = 2
MIDDLE_LEFT = 3
CENTER = 4
MIDDLE_RIGHT = 5
BOTTOM_LEFT = 6
BOTTOM_CENTER = 7
BOTTOM_RIGHT = 8

def print_board(board):
    """Prints the current state of the board."""
    print(f"{board[TOP_LEFT]} | {board[TOP_CENTER]} | {board[TOP_RIGHT]}")
    print("---------")
    print(f"{board[MIDDLE_LEFT]} | {board[CENTER]} | {board[MIDDLE_RIGHT]}")
    print("---------")
    print(f"{board[BOTTOM_LEFT]} | {board[BOTTOM_CENTER]} | {board[BOTTOM_RIGHT]}")

def check_winner(board, player):
    """Checks if the given player has won."""
    win_conditions = [
        [TOP_LEFT, TOP_CENTER, TOP_RIGHT],  # Top row
        [MIDDLE_LEFT, CENTER, MIDDLE_RIGHT],  # Middle row
        [BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT],  # Bottom row
        [TOP_LEFT, MIDDLE_LEFT, BOTTOM_LEFT],  # Left column
        [TOP_CENTER, CENTER, BOTTOM_CENTER],  # Center column
        [TOP_RIGHT, MIDDLE_RIGHT, BOTTOM_RIGHT],  # Right column
        [TOP_LEFT, CENTER, BOTTOM_RIGHT],  # Diagonal from top-left to bottom-right
        [TOP_RIGHT, CENTER, BOTTOM_LEFT]  # Diagonal from top-right to bottom-left
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
            move = input("Enter your move (1-9): ").strip()
            if move.isdigit() and 1 <= int(move) <= 9:
                move = int(move) - 1
                if board[move] == ' ':
                    return move
                else:
                    print(f"Position {move + 1} is already taken. Try again.")
            else:
                print("Invalid input. Please enter a number between 1 and 9.")
        except ValueError:
            print("Please enter a valid number.")

def get_strategic_move(board, player):
    """Gets a strategic move for the computer to block opponent or win."""
    opponent = 'O' if player == 'X' else 'X'
    
    # Check for winning moves
    for i in range(9):
        if board[i] == ' ':
            board_copy = board[:]
            board_copy[i] = player
            if check_winner(board_copy, player):
                return i
    
    # Block opponent's winning move
    for i in range(9):
        if board[i] == ' ':
            board_copy = board[:]
            board_copy[i] = opponent
            if check_winner(board_copy, opponent):
                return i
    
    # Choose a random corner or center if available
    corners = [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT]
    for corner in corners:
        if board[corner] == ' ':
            return corner
    
    if board[CENTER] == ' ':
        return CENTER
    
    # Choose any remaining edge
    edges = [TOP_CENTER, MIDDLE_LEFT, MIDDLE_RIGHT, BOTTOM_CENTER]
    for edge in edges:
        if board[edge] == ' ':
            return edge

def minimax(board, depth, is_maximizing):
    """Implements the minimax algorithm to find the best move."""
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if check_draw(board):
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board_copy = board[:]
                board_copy[i] = 'O'
                score = minimax(board_copy, depth + 1, False)
                board_copy[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board_copy = board[:]
                board_copy[i] = 'X'
                score = minimax(board_copy, depth + 1, True)
                board_copy[i] = ' '
                best_score = min(score, best_score)
        return best_score

def get_minimax_move(board):
    """Gets the move for the computer using the minimax algorithm."""
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board_copy = board[:]
            board_copy[i] = 'O'
            score = minimax(board_copy, 0, False)
            board_copy[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def get_computer_move(board, strategy):
    """Gets a move for the computer based on the chosen strategy."""
    if strategy == 'random':
        available_moves = [i for i, x in enumerate(board) if x == ' ']
        return random.choice(available_moves)
    elif strategy == 'strategic':
        return get_strategic_move(board, 'O')
    elif strategy == 'minimax':
        return get_minimax_move(board)
    else:
        raise ValueError("Invalid strategy. Choose 'random', 'strategic', or 'minimax'.")

def switch_player(current_player):
    """Switches the current player."""
    return 'O' if current_player == 'X' else 'X'

def initialize_game():
    """Initializes the game by setting up the board and choosing a starting player."""
    board = [' '] * 9
    current_player = random.choice(['X', 'O'])  # Randomly choose starting player
    return board, current_player

def get_strategy():
    """Gets the strategy from command line arguments."""
    if len(sys.argv) != 2:
        print("Usage: python tic-tac-toe.py [strategy]")
        print("Strategy options: random, strategic, minimax")
        sys.exit(1)
    return sys.argv[1]

def play_game(board, current_player, strategy):
    """Plays the game loop."""
    while True:
        print_board(board)
        print(f"Current player: {current_player}")
        
        if current_player == 'X':
            move = get_player_move(board)
        else:
            move = get_computer_move(board, strategy)
        
        board[move] = current_player
        print(f"Move made by {current_player} at position {move + 1}")
        
        # Debug print to check player switching
        print(f"Switching from {current_player} to {switch_player(current_player)}")
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = switch_player(current_player)

def main():
    strategy = get_strategy()
    board, current_player = initialize_game()
    play_game(board, current_player, strategy)

if __name__ == "__main__":
    main()

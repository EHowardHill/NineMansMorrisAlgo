# Nine Men's Morris Game with AI opponent
from helper import ( board,
    connections, print_board, print_position_guide,
    check_mill, count_pieces, can_move, remove_opponent_piece
)
from ai import MorrisAI

# Modified main game loop
def play_game():
    global player1_pieces, player2_pieces, player1_placed, player2_placed, current_player, phase
    
    # Game state
    player1_pieces = 9
    player2_pieces = 9
    player1_placed = 0
    player2_placed = 0
    current_player = '1'
    phase = 'placing'
    
    # Get AI difficulty
    print("Welcome to Nine Men's Morris!")
    print("Player 1 (You): '1', Player 2 (AI): '2'")
    print("\nAI Difficulty Levels:")
    print("1 - Beginner (Random moves)")
    print("2 - Easy (Basic strategy)")
    print("3 - Medium (Strategic play)")
    print("4 - Hard (Advanced strategy)")
    print("5 - Expert (Very challenging)")
    
    while True:
        try:
            difficulty = int(input("Choose AI difficulty (1-5): "))
            if 1 <= difficulty <= 5:
                break
            print("Please enter a number between 1 and 5!")
        except:
            print("Please enter a valid number!")
    
    ai = MorrisAI(difficulty)
    print(f"\nYou're playing against AI difficulty level {difficulty}")
    print("Type 'help' anytime to see the position guide.")
    
    while True:
        print_board()
        opponent = '2' if current_player == '1' else '1'
        
        # Check win conditions
        if phase != 'placing':
            if count_pieces(opponent) < 3:
                winner = "You" if current_player == '1' else "AI"
                print(f"{winner} win! Opponent has less than 3 pieces.")
                break
            if not can_move(opponent):
                winner = "You" if current_player == '1' else "AI"
                print(f"{winner} win! Opponent cannot move.")
                break
        
        # Determine game phase
        if player1_placed < 9 or player2_placed < 9:
            phase = 'placing'
        elif count_pieces(current_player) == 3:
            phase = 'flying'
        else:
            phase = 'moving'
        
        if current_player == '1':
            # Human player turn
            print(f"\nYour turn ({phase} phase)")
            
            if phase == 'placing':
                pieces_left = player1_pieces - player1_placed
                print(f"Pieces left to place: {pieces_left}")
                
                while True:
                    move = input("Enter position to place piece (or 'help'): ")
                    if move == 'help':
                        print_position_guide()
                        continue
                    
                    try:
                        pos = int(move)
                        if 0 <= pos <= 23 and board[pos] == ' ':
                            board[pos] = current_player
                            player1_placed += 1
                            
                            if check_mill(pos, current_player):
                                print_board()
                                remove_opponent_piece(opponent)
                            break
                        else:
                            print("Invalid position! Choose an empty spot (0-23).")
                    except:
                        print("Please enter a valid number or 'help'!")
            
            else:  # Moving or flying phase
                if phase == 'flying':
                    print("Flying phase - you can move to any empty position!")
                
                while True:
                    move = input("Enter move as 'from to' (e.g., '0 1') or 'help': ")
                    if move == 'help':
                        print_position_guide()
                        continue
                    
                    try:
                        parts = move.split()
                        if len(parts) == 2:
                            from_pos = int(parts[0])
                            to_pos = int(parts[1])
                            
                            if (0 <= from_pos <= 23 and 0 <= to_pos <= 23 and
                                board[from_pos] == current_player and board[to_pos] == ' '):
                                
                                if phase == 'flying' or to_pos in connections[from_pos]:
                                    board[from_pos] = ' '
                                    board[to_pos] = current_player
                                    
                                    if check_mill(to_pos, current_player):
                                        print_board()
                                        remove_opponent_piece(opponent)
                                    break
                                else:
                                    print("You can only move to adjacent positions!")
                            else:
                                print("Invalid move! Check your positions.")
                        else:
                            print("Enter move as two numbers separated by space!")
                    except:
                        print("Please enter valid numbers!")
        
        else:
            # AI player turn
            print(f"\nAI's turn ({phase} phase)")
            
            if phase == 'placing':
                pieces_left = player2_pieces - player2_placed
                print(f"AI pieces left to place: {pieces_left}")
                
                pos = ai.make_move(phase, pieces_left)
                if pos is not None:
                    print(f"AI places piece at position {pos}")
                    board[pos] = current_player
                    player2_placed += 1
                    
                    if check_mill(pos, current_player):
                        print_board()
                        print("AI formed a mill!")
                        # AI chooses piece to remove
                        target = ai.choose_piece_to_remove()
                        if target is not None:
                            print(f"AI removes your piece at position {target}")
                            board[target] = ' '
            
            else:  # Moving or flying phase
                if phase == 'flying':
                    print("AI is in flying phase!")
                
                move = ai.make_move(phase)
                if move:
                    from_pos, to_pos = move
                    print(f"AI moves piece from {from_pos} to {to_pos}")
                    board[from_pos] = ' '
                    board[to_pos] = current_player
                    
                    if check_mill(to_pos, current_player):
                        print_board()
                        print("AI formed a mill!")
                        target = ai.choose_piece_to_remove()
                        if target is not None:
                            print(f"AI removes your piece at position {target}")
                            board[target] = ' '
        
        # Switch players
        current_player = '2' if current_player == '1' else '1'
    
    print("\nGame Over! Thanks for playing!")

# Run the game
if __name__ == "__main__":
    play_game()
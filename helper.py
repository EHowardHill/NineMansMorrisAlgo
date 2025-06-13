board = [' '] * 24

# Define board connections (adjacent positions)
connections = {
    0: [1, 9], 1: [0, 2, 4], 2: [1, 14],
    3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
    6: [7, 11], 7: [4, 6, 8], 8: [7, 12],
    9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15],
    12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
    15: [11, 16], 16: [15, 17, 19], 17: [12, 16],
    18: [10, 19], 19: [16, 18, 20, 22], 20: [13, 19],
    21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
}

# Define mill combinations
mills = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Outer square
    [9, 10, 11], [12, 13, 14], [15, 16, 17],  # Middle square
    [18, 19, 20], [21, 22, 23],  # Inner square
    [0, 9, 21], [3, 10, 18], [6, 11, 15],  # Left connections
    [1, 4, 7], [16, 19, 22],  # Middle connections
    [8, 12, 17], [5, 13, 20], [2, 14, 23]  # Right connections
]

def print_board():
    print("\n" + board[0] + "----------" + board[1] + "----------" + board[2])
    print("|          |          |")
    print("|   " + board[3] + "------" + board[4] + "------" + board[5] + "   |")
    print("|   |      |      |   |")
    print("|   |  " + board[6] + "---" + board[7] + "---" + board[8] + "  |   |")
    print("|   |  |       |  |   |")
    print(board[9] + "---" + board[10] + "--" + board[11] + "       " + board[15] + "--" + board[16] + "---" + board[17])
    print("|   |  |       |  |   |")
    print("|   |  " + board[18] + "---" + board[19] + "---" + board[20] + "  |   |")
    print("|   |      |      |   |")
    print("|   " + board[21] + "------" + board[22] + "------" + board[23] + "   |")
    print("|          |          |")
    print(board[12] + "----------" + board[13] + "----------" + board[14] + "\n")

def print_position_guide():
    print("\nPosition Guide:")
    print("0----------1----------2")
    print("|          |          |")
    print("|   3------4------5   |")
    print("|   |      |      |   |")
    print("|   |  6---7---8  |   |")
    print("|   |  |       |  |   |")
    print("9---10-11      15-16--17")
    print("|   |  |       |  |   |")
    print("|   |  18--19--20 |   |")
    print("|   |      |      |   |")
    print("|   21-----22-----23  |")
    print("|          |          |")
    print("12---------13---------14\n")

def check_mill(pos, player):
    for mill in mills:
        if pos in mill and all(board[p] == player for p in mill):
            return True
    return False

def count_pieces(player):
    return sum(1 for p in board if p == player)

def can_move(player):
    if count_pieces(player) == 3:  # Flying phase
        return any(board[i] == ' ' for i in range(24))
    
    for i in range(24):
        if board[i] == player:
            for neighbor in connections[i]:
                if board[neighbor] == ' ':
                    return True
    return False

def remove_opponent_piece(opponent):
    print("You formed a mill! Remove an opponent's piece.")
    
    # Find removable pieces (not in a mill unless all pieces are in mills)
    removable = []
    all_in_mills = []
    
    for i in range(24):
        if board[i] == opponent:
            if not check_mill(i, opponent):
                removable.append(i)
            all_in_mills.append(i)
    
    if not removable:
        removable = all_in_mills
    
    if not removable:
        print("No pieces to remove!")
        return
    
    print("Opponent pieces at positions:", removable)
    
    while True:
        try:
            pos = int(input("Enter position to remove: "))
            if pos in removable:
                board[pos] = ' '
                print("Piece removed!")
                break
            else:
                print("Invalid position! Choose from:", removable)
        except:
            print("Please enter a valid number!")

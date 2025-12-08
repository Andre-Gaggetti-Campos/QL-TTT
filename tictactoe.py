import sys

def generateBoard(size, state):

    counterMain = 0
    print("\n")

    for i in range(size):

        print("____"*size, end="_\n")
        print("|   "*size, end="|\n")

        for j in range(size):
            print("| " + state[counterMain] + " ", end="")
            counterMain += 1

        print("|", end="\n")

    print("____"*size, end="_\n")

def checkBoardState(size, state):

    win_len = 3 if size == 3 else 4 if size == 5 else size

    # Horizontal
    for row in range(size):
        for col in range(size - win_len + 1):
            segment = state[row*size + col : row*size + col + win_len]
            if segment[0] != " " and all(c == segment[0] for c in segment):
                return "Win"

    # Vertical
    for col in range(size):
        for row in range(size - win_len + 1):
            segment = [state[(row+i)*size + col] for i in range(win_len)]
            if segment[0] != " " and all(c == segment[0] for c in segment):
                return "Win"

    # Diagonal
    for row in range(size - win_len + 1):
        for col in range(size - win_len + 1):
            segment = [state[(row+i)*size + (col+i)] for i in range(win_len)]
            if segment[0] != " " and all(c == segment[0] for c in segment):
                return "Win"

    # Anti-diagonal
    for row in range(size - win_len + 1):
        for col in range(win_len - 1, size):
            segment = [state[(row+i)*size + (col-i)] for i in range(win_len)]
            if segment[0] != " " and all(c == segment[0] for c in segment):
                return "Win"

    if " " not in state:
        return "Draw"

    return "Undeclared"

def soloPlay():
    
    while True:

        print("\nBoard side length? (Note 5x5 will have 4 in a row to win, otherwise NxN will have n in a row to win)")

        size_choice = input("> ")

        if size_choice == "Exit": 
            print("Exiting...")
            sys.exit()

        try:
            size = int(size_choice)
        except ValueError:
            print("Side length must be a number.")
            continue

        if size > 2:
            break
        else:
            print("Side length must be greater than 2. Try again.")

    state = [" "]*(size*size)
    generateBoard(size, state)

    turn = "X"

    while True:
        
        print(f"\nPlayer {turn}'s turn. Enter position 1,1 to {int(size)},{int(size)}:")
        input_pos = input("> ")

        if input_pos == "Exit": 
            print("Exiting...")
            sys.exit()

        pos_split = input_pos.split(",")

        if len(pos_split) != 2:
            print("Please enter position in the format row,column (e.g., 1,1).")
            continue

        row, col = pos_split

        try:
            row = int(row) - 1
            col = int(col) - 1
        except ValueError:
            print("Row and Column must be numbers. Try again.")
            continue

        if not (0 <= row < size and 0 <= col < size):
            print("Position out of bounds. Try again.")
            continue

        pos = col * size + row

        if state[pos] == " ":
            
            state[pos] = turn
            generateBoard(size, state)

            outcome = checkBoardState(size, state)

            if outcome == "Win":
                print(f"\nPlayer {turn} has won.")
                break

            if outcome == "Draw":
                print("\nThe game is a draw.")
                break

            turn = "O" if turn == "X" else "X"
        else:
            print("Invalid position. Try again.")
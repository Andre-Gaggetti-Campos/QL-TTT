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

    # Horizontal Checks
    for row in range(size):
        counter = 1
        for col in range(1, size):
            curr = state[row*size + col]
            prev = state[row*size + col - 1]

            if curr != " " and curr == prev:
                counter += 1
                if counter == 3:
                    return "Win"
            else:
                counter = 1

    # Vertical Checks
    for col in range(size):
        counter = 1
        for row in range(1, size):
            curr = state[row*size + col]
            prev = state[(row-1)*size + col]

            if curr != " " and curr == prev:
                counter += 1
                if counter == 3:
                    return "Win"
            else:
                counter = 1

    # Diagonal Checks
    for row in range(1, size - 1):
        for col in range(1, size - 1):
            curr = state[row*size + col]
            if curr != " " and curr == state[(row-1)*size + (col-1)] and curr == state[(row+1)*size + (col+1)]:
                return "Win"
            if curr != " " and curr == state[(row-1)*size + (col+1)] and curr == state[(row+1)*size + (col-1)]:
                return "Win"
            
    # Check for Draw
    if " " not in state:
        return "Draw"

    return "Undeclared"

def soloPlay():
    print("\nBoard size?")
    print("1. 3x3")
    print("2. 5x5")
    size_choice = input("> ")
    if size_choice == "1" or size_choice == "2":
        size = 3 if size_choice == "1" else 5
        state = [" "]*(size*size)
        generateBoard(size, state)
    else:
        print("Exiting...")
        if size_choice == "Exit": sys.exit()

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
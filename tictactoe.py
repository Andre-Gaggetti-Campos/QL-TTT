def generateBoard(size, state):
    counterMain = 0
    counterExample = 1
    print("\n")
    for i in range(size):

        print("____"*size, end="_")

        print("    "+"____"*size, end="_\n")

        print("|   "*size, end="|")

        print("    "+"|   "*size, end="|\n")

        for j in range(size):
            print("| " + state[counterMain] + " ", end="")
            counterMain += 1
        print("|", end="")

        print("    ", end="")
        for j in range(size):
            print("| " + str(counterExample%10) + " ", end="")
            counterExample += 1
        print("|", end="\n")

    print("____"*size, end="_")

    print("    "+"____"*size, end="_\n")

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
        
testing_state_3x3 = [
    "X", "O", "X",
    " ", "X", "O",
    "O", " ", "X"
]

testing_state_5x5 = [
    "X", "O", "X", " ", "O",
    " ", "X", "O", "X", " ",
    "O", " ", "X", "O", "X",
    "X", "O", " ", "X", " ",
    "O", "X", "O", " ", "X"
]

def soloplay():
    print("\nBoard size?")
    print("1. 3x3")
    print("2. 5x5")
    size_choice = input("> ")
    if size_choice == "1" or size_choice == "2":
        size = 3 if size_choice == "1" else 5
        state = [" "]*(size*size)
        generateBoard(size, state)

    turn = "X"

    while True:
        print(f"\nPlayer {turn}'s turn. Enter position (1-{size*size}):")
        pos = input("> ")
        if pos.isdigit():
            pos = int(pos) - 1
            if 0 <= pos < size*size and state[pos] == " ":
                print(f"Player {turn} chose position {pos + 1}.")
            
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
        else:
            print("Please enter a valid number.")
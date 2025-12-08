import tictactoe as ttt
import sys

def main():
    print("\n=== Welcome to Q-Learning Tic Tac Toe! ===")

    while True:
        print("\nMenu:")
        print("1. Solo Play")
        print("2. Play vs Bot")
        print("3. Bot vs Bot")
        print("4. Train/View Bots")
        print("Type 'Exit' to leave at any point")

        choice = input("> ")

        if choice == "1":
            ttt.soloPlay()
        if choice == "Exit":
            print("Exiting...")
            sys.exit()
        
if __name__ == "__main__":
    main()
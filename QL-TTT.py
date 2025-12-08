import tictactoe as ttt

def main():
    print("\n=== Welcome to Q-Learning Tic Tac Toe! ===")

    while True:
        print("\nMenu:")
        print("1. Solo Play")
        print("2. Play vs Bot")
        print("3. Bot vs Bot")
        print("4. Train/View Bots")
        print("5. Exit")
        choice = input("> ")

        if choice == "1":
            ttt.soloplay()
        
if __name__ == "__main__":
    main()
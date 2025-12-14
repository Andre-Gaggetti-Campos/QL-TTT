import os
import sys
import json
import random
from tqdm import tqdm
from .tictactoe import checkBoardState, generateBoard

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_executable_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

botDirectory = os.path.join(get_executable_dir(), "bots")
os.makedirs(botDirectory, exist_ok=True)

class QBot:

    def __init__(self, name, alpha, gamma, epsilon, board_size, episodes=0):
        self.name = name
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.board_size = board_size
        self.episodes = episodes
        self.q_table = {}

    def toDict(self):
        return {
            "name": self.name,
            "alpha": self.alpha,
            "gamma": self.gamma,
            "epsilon": self.epsilon,
            "board_size": self.board_size,
            "episodes": self.episodes,
            "q_table": self.q_table
        }

    def fromDict(self, data):
        self.name = data["name"]
        self.alpha = data["alpha"]
        self.gamma = data["gamma"]
        self.epsilon = data["epsilon"]
        self.board_size = data["board_size"]
        self.episodes = data["episodes"]
        self.q_table = data["q_table"]

def saveBots(bot):

    path = os.path.join(botDirectory, f"{bot.name}.json")
    with open(path, "w") as f:
        json.dump(bot.toDict(), f)

def loadBots():
    
    bots = []

    for file in os.listdir(botDirectory):
        if file.endswith(".json"):
            with open(os.path.join(botDirectory, file), "r") as f:
                data = json.load(f)
                bot = QBot("", 0, 0, 0, 0)
                bot.fromDict(data)
                bots.append(bot)

    return bots

def chooseAction(state, bot):

    available_actions = [i for i, v in enumerate(state) if v == " "]

    if random.uniform(0, 1) < bot.epsilon or state not in bot.q_table:
        return random.choice(available_actions)

    q_values = bot.q_table.get(state, {})
    q_values = {a: q for a, q in q_values.items() if a in available_actions}

    if not q_values:
        return random.choice(available_actions)

    max_q = max(q_values.values())
    best_actions = [a for a, q in q_values.items() if q == max_q]
    
    return random.choice(best_actions)
    
    
def updateQValue(bot, state, action, reward, next_state):

    current_q = bot.q_table.get(state, {}).get(action, 0)
    next_max_q = 0

    if next_state in bot.q_table:
        next_max_q = max(bot.q_table[next_state].values())

    new_q = current_q + bot.alpha * (reward + bot.gamma * next_max_q - current_q)

    if state not in bot.q_table:
        bot.q_table[state] = {}

    bot.q_table[state][action] = new_q

def playSelf(bot, size):

    board = [" "] * (size * size)
    turn = "X"
    bot_marker = random.choice(["X", "O"])
    opp_marker = "O" if bot_marker == "X" else "X"
    last_bot_action = None

    def oppCanWin(b, marker):

        for i, v in enumerate(b):
            if v == " ":
                b[i] = marker
                if checkBoardState(size, b) == "Win":
                    b[i] = " "
                    return True
                b[i] = " "
        return False

    while True:

        state_before = "".join(board)
        available_actions = [i for i, v in enumerate(board) if v == " "]

        if turn == bot_marker:

            action = chooseAction(state_before, bot)
            board[action] = bot_marker
            next_state = "".join(board)

            result = checkBoardState(size, board)

            if result == "Win":

                reward = 1
                updateQValue(bot, state_before, action, reward, next_state)
                return 1
            
            elif result == "Draw":

                reward = 0
                updateQValue(bot, state_before, action, reward, next_state)
                return 0
            
            else:

                reward = 0
                if oppCanWin(board, opp_marker):
                    reward = -0.5
                updateQValue(bot, state_before, action, reward, next_state)

            last_bot_action = action

        else:

            move_made = False

            for i in available_actions:
                board[i] = opp_marker
                if checkBoardState(size, board) == "Win":
                    move_made = True
                    break
                board[i] = " "

            if not move_made:

                action = random.choice(available_actions)
                board[action] = opp_marker

            result = checkBoardState(size, board)

            if result == "Win":

                reward = -1
                if last_bot_action is not None:
                    updateQValue(bot, state_before, last_bot_action, reward, "".join(board))
                return -1
            
            elif result == "Draw":
                reward = 0
                if last_bot_action is not None:
                    updateQValue(bot, state_before, last_bot_action, reward, "".join(board))
                return 0

        turn = "O" if turn == "X" else "X"

def trainBot(bot, episodes, size=None, save_every=500):
    if size is None:
        size = bot.board_size

    wins = 0
    losses = 0
    draws = 0

    decay_rate = 0.999995
    min_epsilon = 0.05

    print(f"\nTraining bot '{bot.name}' for {episodes} episodes...")

    with tqdm(total=episodes, ncols=80, desc=f"Training {bot.name}") as pbar:
        for ep in range(1, episodes + 1):
            result = playSelf(bot, size)

            if result == 1:
                wins += 1
            elif result == -1:
                losses += 1
            else:
                draws += 1

            bot.epsilon = max(min_epsilon, bot.epsilon * decay_rate)
            bot.episodes += 1

            pbar.set_postfix({"W": wins, "L": losses, "D": draws, "eps": f"{bot.epsilon:.3f}"})
            pbar.update(1)

            if ep % save_every == 0:
                saveBots(bot)

    saveBots(bot)

    print(f"\nTraining complete. Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Final epsilon: {bot.epsilon:.3f}\n")

def createBot():

    print("\n=== Create a New Q-Learning Bot ===")
    name = input("Bot name: ")

    while True:
        try:
            alpha = float(input("Learning rate α (0.0-1.0): "))
            if 0 <= alpha <= 1:
                break
            print("Alpha must be between 0 and 1.")
        except ValueError:
            print("Enter a valid number.")

    while True:
        try:
            gamma = float(input("Discount factor γ (0.0-1.0): "))
            if 0 <= gamma <= 1:
                break
            print("Gamma must be between 0 and 1.")
        except ValueError:
            print("Enter a valid number.")

    while True:
        try:
            epsilon = float(input("Exploration rate ε (0.0-1.0): "))
            if 0 <= epsilon <= 1:
                break
            print("Epsilon must be between 0 and 1.")
        except ValueError:
            print("Enter a valid number.")

    while True:
        try:
            size = int(input("Board size N (e.g., 3 for 3x3): "))
            if size >= 3:
                break
            print("Board size must be 3 or greater.")
        except ValueError:
            print("Enter a valid number.")

    new_bot = QBot(name, alpha, gamma, epsilon, size)
    saveBots(new_bot)
    print(f"\nBot '{name}' created and saved successfully!\n")
    return new_bot


def playVersusBot(bot, size=None, human_first=None):

    if size is None:
        size = bot.board_size

    board = [" "] * (size * size)

    if human_first is None:
        turn = random.choice(["X", "O"])
    else:
        turn = "X" if human_first else "O"

    human_marker = "X" if turn == "X" else "O"
    bot_marker = "O" if human_marker == "X" else "X"

    print(f"\nYou are '{human_marker}'. Bot ({bot.name}) is '{bot_marker}'.\n")
    generateBoard(size, board)

    while True:

        available = [i for i, v in enumerate(board) if v == " "]

        if turn == bot_marker:

            action = chooseAction("".join(board), bot)
            board[action] = bot_marker
            print(f"\nBot plays at position {action // size + 1},{action % size + 1}")

        else:

            move = input("\nYour move (row,col) or 'Exit': ")
            if move.lower() == "exit":
                print("Exiting game.")
                return
            try:
                r, c = map(int, move.split(","))
                if not (0 <= r-1 < size and 0 <= c-1 < size):
                    print("Out of bounds, try again.")
                    continue
                pos = (r-1) * size + (c-1)
                if board[pos] != " ":
                    print("Space occupied, try again.")
                    continue
            except:
                print("Invalid input, use row,col format.")
                continue
            board[pos] = human_marker

        generateBoard(size, board)

        result = checkBoardState(size, board)

        if result == "Win":
            if turn == bot_marker:
                print("\nBot wins!")
            else:
                print("\nYou win!")
            return
        elif result == "Draw":
            print("\nIt's a draw!")
            return

        turn = "O" if turn == "X" else "X"

def botVersusBot(bot1, bot2, games, size=None):
    if size is None:
        size = bot1.board_size

    x_wins = 0
    o_wins = 0
    draws = 0

    print(f"\nBot vs Bot: {bot1.name} (X) vs {bot2.name} (O)\n")

    for g in range(1, games+1):
        board = [" "] * (size*size)
        turn = "X"

        while True:
            available = [i for i, v in enumerate(board) if v == " "]

            if turn == "X":
                action = chooseAction("".join(board), bot1)
                board[action] = "X"
            else:
                action = chooseAction("".join(board), bot2)
                board[action] = "O"

            result = checkBoardState(size, board)

            if result == "Win":
                if turn == "X":
                    x_wins += 1
                else:
                    o_wins += 1
                break
            elif result == "Draw":
                draws += 1
                break

            turn = "O" if turn == "X" else "X"

    print("\n=== Results ===")
    print(f"{bot1.name} (X) wins: {x_wins}")
    print(f"{bot2.name} (O) wins: {o_wins}")
    print(f"Draws: {draws}\n")


def manageBots():
    while True:
        print("\n=== Bot Manager ===")
        print("1. Create New Bot")
        print("2. Train Existing Bot")
        print("3. Return")

        choice = input("> ")

        if choice == "1":
            createBot()

        elif choice == "2":
            bots = loadBots()
            if not bots:
                print("No bots found. Create a bot first.")
                continue

            print("\nSelect bot to train:")
            for i, b in enumerate(bots):
                print(f"{i+1}. {b.name} | episodes: {b.episodes} | epsilon: {b.epsilon:.3f}")

            try:
                idx = int(input("> ")) - 1
                if not (0 <= idx < len(bots)):
                    print("Invalid selection.")
                    continue
            except:
                print("Invalid input.")
                continue

            try:
                episodes = int(input("Episodes to train: "))
            except:
                print("Invalid input for episodes.")
                continue

            trainBot(bots[idx], episodes)

        elif choice == "3":
            print("Returning to main menu...")
            return
        
        elif choice == "Exit":
            print("Exiting...")
            sys.exit()

        else:
            print("Invalid choice. Enter 1, 2, or 3.")

def playVsBotDialogue():
    bots = loadBots()
    if not bots:
        print("No bots found. Create a bot first.")
        return

    print("\nSelect a bot to play against:")
    for i, b in enumerate(bots):
        print(f"{i+1}. {b.name} | episodes trained: {b.episodes} | epsilon: {b.epsilon:.3f}")

    try:
        idx = int(input("> ")) - 1
        if not (0 <= idx < len(bots)):
            print("Invalid selection.")
            return
    except:
        print("Invalid input.")
        return

    bot = bots[idx]
    print(f"\nYou will play against {bot.name}.")

    while True:
        first = input("Do you want to go first? (y/n): ").lower()
        if first in ["y", "n"]:
            break
        print("Enter 'y' or 'n'.")

    if first == "y":
        human_first = True
    else:
        human_first = False

    playVersusBot(bot, human_first=human_first)

def botVsBotDialogue():
    
    bots = loadBots()
    if len(bots) < 2:
        print("Need at least 2 bots to run a bot vs bot match.")
        return

    print("\nSelect Bot 1 (X):")
    for i, b in enumerate(bots):
        print(f"{i+1}. {b.name}")
    try:
        idx1 = int(input("> ")) - 1
        if not (0 <= idx1 < len(bots)):
            print("Invalid selection.")
            return
    except:
        print("Invalid input.")
        return

    print("\nSelect Bot 2 (O):")
    for i, b in enumerate(bots):
        print(f"{i+1}. {b.name}")
    try:
        idx2 = int(input("> ")) - 1
        if not (0 <= idx2 < len(bots)) or idx2 == idx1:
            print("Invalid selection.")
            return
    except:
        print("Invalid input.")
        return

    try:
        games = int(input("\nEnter number of games to simulate: "))
    except:
        print("Invalid input for number of games.")
        return

    botVersusBot(bots[idx1], bots[idx2], games)
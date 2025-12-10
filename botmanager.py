import os
import json
import random
from tqdm import tqdm
from tictactoe import checkBoardState, generateBoard

botDirectory = "bots"
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

#def chooseAction(bot, state, available_actions):

#def updateQ(bot, state, action, reward, next_state, available_actions):

#def playSelf(bot, size):

#def trainBot(bot, episodes):

#def botVersusBot(bot1, bot2, games):

#def playVersusBot(bot, size):
# QL-TTT

Q-Learning-TicTacToe (or QL-TTT) is an inline CLI program where users can train bots with customizable conditions, pitch the bots against eachother, play against a bot, or play by themselves, all in any sized square TicTacToe environment.

---

## Quick Start (End Users)

1. Download the latest release executable from GitHub Releases.
2. Run the executable (`QL-TTT.exe` on Windows, or the respective binary for your OS).
3. Bots will be stored automatically in a `bots/` folder created next to the executable.
4. Play, train, and enjoy!

## Installation (Developers / Source Code)

1. **Clone the repository:**

```bash
git clone https://github.com/Andre-Gaggetti-Campos/QL-TTT.git
cd QL-TTT
```

2. **(Optional) Create a Virtual Environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run From Source**

```bash
cd src
python -m ql_ttt
```

5. **Build The Executable**

```bash
pyinstaller --clean --onefile --hidden-import tqdm --name QL-TTT src/ql_ttt.py
```

---

## Repository Structure

```CSS
QL-TTT/
├── src/
│   ├── ql_ttt.py
│   ├── botmanager.py
│   └── tictactoe.py
├── .gitignore
├── README.md
├── LICENSE.md
├── requirements.txt
└── bots/              ← runtime-generated, ignored in Git
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

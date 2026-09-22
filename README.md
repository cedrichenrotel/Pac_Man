> *This project was created as part of the 42 curriculum by **cehenrot** and **matgiber**.*

# Pac-Man ᗧ···ᗣ···ᗣ

## Description
This project is a fully playable remake of the classic Pac-Man game, written in Python using Object-Oriented Programming (OOP) principles. 

The graphical interface is built using 42's **MiniLibX**, integrated into Python. The application is designed to be easily exportable as a standalone executable. The game is highly customizable via a configuration file (`config.json`), features a non-blocking error logging system, and includes built-in cheat codes to facilitate testing and debugging.

## Installation & Usage

### Prerequisites
The project uses `uv` as a package manager to handle all necessary libraries. 

### Installation
To clone and set up the project, run:
```bash
make install
# or simply
make
```
*This command will launch `uv` and automatically install all required project dependencies.*

### Running the Game
To launch the game, you need to provide the configuration file as an argument:
```bash
make run
# or
python3 pac-man.py config.json
```

---

## Configuration (`config.json`)

A configuration file is required to launch the project. If certain fields are missing, the game will automatically apply default values and display non-blocking warnings in the console to inform the user.

### Example `config.json`
```json
{
    "highscore_filename": "highscore.json",
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
    "level": {
        "width": 15,
        "height": 15
    }
}
```

### Parameters
* **`highscore_filename`**: Name of the file where high scores are saved (default: `"highscore.json"`).
* **`lives`**: Number of lives the player starts with (default: `3`).
* **`pacgum`**: Number of Pac-Gums the player must eat to complete the level (default: `42`).
* **`points_per_pacgum`**: Points awarded per Pac-Gum eaten (default: `10`).
* **`points_per_super_pacgum`**: Points awarded per Super Pac-Gum eaten (default: `50`).
* **`points_per_ghost`**: Points awarded for eating a vulnerable ghost (default: `200`).
* **`seed`**: Seed used for maze generation (default: `42`).
* **`level_max_time`**: Time limit per level in seconds. If the timer runs out before eating the required Pac-Gums, the player loses (default: `90`).
* **`level`** (`width`, `height`): Dimensions of the maze for each level (default: `15x15`).

---

## Key Features

### Highscore System
The game features a secure JSON-based high score system. 
* At the end of every game, the player's score is pushed to the file.
* The system automatically sorts the scores in descending order.
* Only the **top 10** scores are kept and saved.
* Players can view the top 10 scoreboard at any time via the `"View Highscore"` option in the main menu.

### Maze Generation
The labyrinths are generated using the maze generation package provided by 42 school. 
It is installed via `uv` and integrated into the project just like a standard Python library:
```python
from mazegenerator import MazeGenerator
```

---

## General Software Architecture

* The project is structured around strict Object-Oriented Programming (OOP) principles to ensure scalability, readability, and modularity.
* The architecture clearly separates the game engine logic from the graphical rendering system based on MiniLibX 42.
* Game entities (Pac-Man, ghosts, collectibles) are modeled by inherited classes. These classes encapsulate their specific movement, collision, and sprite management logic.
* Maze generation relies on the external 42 school package `mazegenerator`. The system caches the results of these generated levels as images.

## Implementation 

* **Dependencies and Environment:** The project uses `uv` as the main dependency manager. The specific packages `mazegenerator` and `mlx` are configured to be sourced from local `.whl` files, with `mlx` installation being resolved dynamically depending on the platform (macOS or Linux).
* **Data Control and Validation:** Initial parameters (lives, level duration, maze size) are isolated in the config.json file. This file is strictly mandatory for the application to function and must contain at least an empty JSON object ({}). The pydantic dependency declared in the project configuration suggests strict type and structure validation for this incoming data. The persistent state (high scores) is read and updated in JSON format in highscore.json.
* **Development Tools:** A `Makefile` exposes common commands such as installation, starting the game, or interactive debugging (`python -m pdb`).
* **Code Quality:** The implementation enforces rigorous checking through linting. Strict `mypy` rules (notably `--disallow-untyped-defs`) as well as `flake8` and `ruff` are configured to be executed via the `Makefile` or set up in `pyproject.toml`.
* **Build System:** The project relies on `pyinstaller` to produce a standalone binary. The deployment script `export.sh` automates this process and dynamically generates a hook (`runtime_hook.py`) that injects the default configuration file when the application runs in an unpacked environment (via `sys._MEIPASS`). The build specification explicitly includes `assets`, forces the full collection of `mlx`, and generates a console interface program.

---

## Resources & Acknowledgments

* **MiniLibX Documentation**: [Harm Smits 42 Docs](https://harm-smits.github.io/42docs/)
* **MiniLibX Python Wrapper**: See `Pac_Man/docs/doc_mlx.md` for our internal Python wrapper documentation.
* **Executable Generation**: [PyInstaller Tutorial](https://medium.com/@arhamrumi/build-a-one-file-exe-with-pyinstaller-including-binaries-resources-760bcffe30ab) by Arham Rumi (used to bundle the project into a standalone `.exe`).

### AI Usage Disclosure
*Claude AI was used during the development of this project strictly as an advanced search engine and learning assistant to break down complex topics. All AI-generated explanations and suggestions were manually verified, tested, and fully understood by the authors prior to implementation in the codebase.*

## Project Management

The project was organized around extensive peer reviews for each implementation.

Each feature was discussed and agreed upon collectively throughout the development process. Every feature was developed on its own branch and reviewed through a Pull Request before being merged into the `main` branch.

A significant amount of verbal communication and discussion took place throughout the project. This allowed us to coordinate effectively without the need for a formal timeline or project management tools such as Jira.

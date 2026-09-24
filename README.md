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

Voici une proposition de texte, en anglais comme le reste du README. Je l'ai construite à partir des 28 PR fusionnées (#1 → #32) et de l'auteur des commits dans chaque branche. Mateo apparaît sous plusieurs identités git (matgiber, ewa, Mateo, Mateo Gibert) et je les ai regroupées sous son nom.

## Project Management

The project was organized around extensive peer reviews for each implementation.

Each feature was discussed and agreed upon collectively throughout the development process. Every feature was developed on its own branch and reviewed through a Pull Request before being merged into the `main` branch. As a rule, the Pull Requests of one team member were reviewed and merged by the other (28 Pull Requests merged in total).

A significant amount of verbal communication and discussion took place throughout the project. This allowed us to coordinate effectively without the need for a formal timeline or project management tools such as Jira.

### Task distribution

**Cédric Henrotel (`cedrichenrotel`)**
* Project bootstrap: `main` entry point and `config.json` parser (comment handling, validation) — PR #1, #2
* Integration of the `mazegenerator` package and initialization of maze elements (Pac-Man, ghosts, pac-gums, super pac-gums) — PR #2, #5
* Entity class hierarchy (`Entity`, `Pacman`, `Ghost`) using polymorphism — PR #5
* Maze and elements rendering, resolution handling — PR #8
* Pac-Man movement, key bindings and sprite animations — PR #9, #12
* Pac-gum / super pac-gum logic, ghost vulnerability (blue ghosts) and timer — PR #16
* Pac-Man eating ghosts: ghost respawn, flashing, death sprite — PR #18
* Project restructuring (`level.py` refactor, `draw` module) — PR #20
* Cheat codes and their on-screen display, level timer — PR #22
* Win / Game Over screens, waiting time and blinking display — PR #26
* Debugging, refactoring (ghost movement, render utils, duplicate removal), maze size safety — PR #29, #30
* Fixes on the new pac-gum system (reset on life loss, countdown, lint) — PR #32

**Mateo Gibert (`matgiber`)**
* MiniLibX setup, `Game` / scene architecture, main menu (selector, logo, colors, error messages) — PR #4
* Folder structure split into `engine` / `render`, level logic and `GameEngine` class — PR #6
* Ghost pathfinding algorithm (DFS) — PR #7, later optimized in PR #13, #23
* Highscore system (`highscore.json` persistence and display) — PR #10
* Ghost / Pac-Man collision detection, lives display — PR #13
* Instructions page — PR #14
* Player name input page and score recording — PR #17
* Rendering and game-loop optimization, HUD on canvas, window close handling — PR #21
* Fleeing ghosts algorithm and level win detection — PR #23
* Pause menu, macOS/Linux `mlx` support in `pyproject.toml` — PR #24
* Launch file, build/export command (`pyinstaller`), score fixes — PR #25
* README writing — PR #27, #28
* Refactoring of positioning, ghost side bug fix — PR #28
* New pac-gum system with a limit based on maze size, timer paused during pause menu — PR #31, #32

**Shared work**
* Code reviews on every Pull Request
* Linting and typing compliance (`flake8`, `mypy`, `ruff`) on both sides

À vérifier avant de coller le texte :
- #2 : ce numéro est une supposition. Le merge « CH_integration_genrator et initialisation_element_labyrinthe » n'a pas de numéro dans le log, donc tu peux le supprimer ou le corriger.
- Répartition de #32 : Mateo a créé le nouveau système de pac-gums et tu as corrigé les bugs. C'est ce que j'ai écras comme ça que ça s'est passé.
- Commits sur les branches de l'autre : quelques commits ont été faits sur la branche de l'autre personne (par exemple ta correction de l'algo « manhattan » dans #23). Je les ai laissés de côté pour que la liste reste lisible.

Tu veux que je l'insère directement dans le README.md ou tu préfères le coller toi-même ?
### Maze Generation
The labyrinths are generated with the **`mazegenerator`** package (v2.1.0), which comes from the A-Maze-ing project. It is shipped as a wheel in `lib/`, declared as a local dependency in `pyproject.toml`, and installed by `uv` like any other Python library:

```python
from mazegenerator import MazeGenerator
```

#### How it is used
* **Creation**: `Level.generate_maze()` builds a `MazeGenerator` from the `width`/`height` in `config.json` and a seed:
  ```python
  MazeGenerator(size=(width, height), seed=seed)
  ```
* **Seed & levels**: The first level uses the `seed` from the config. Each new level uses `seed + level_number`, so every level has a different layout but the same seed always rebuilds the same sequence of mazes.
* **Pac-Man compatible**: The package is used in its non-perfect mode (the default). After the maze is carved, a *braiding* step removes every dead end, which makes loops so the player can never be trapped by a ghost.
* **"42" pattern**: The generator puts a closed "42" shape in the middle of the maze. Its cells are fully walled (value `15`), and nothing can walk through them or spawn on them.

#### Maze representation
The generated grid is available through `generator.maze`, a 2D list (`maze[y][x]`) of integers. Each cell stores its walls as a bitmask:

| Bit | Value | Wall  |
|-----|-------|-------|
| 0   | 1     | North |
| 1   | 2     | East  |
| 2   | 4     | South |
| 3   | 8     | West  |

A move is allowed when the wall bit for that direction is not set (`maze[y][x] & code == 0`). Entity movement, ghost pathfinding and maze rendering all rely on this encoding.

#### Placing the game elements
Once the maze exists, `InitMaze` fills it using the configuration:
* **Pac-Man** spawns at the center of the maze.
* **Ghosts** spawn in the four corners.
* **Super Pac-Gums** are placed in the four corners.
* **Pac-Gums** are spread randomly over the walkable cells that are left (not `15` and not reserved). If `pacgum` is higher than the number of free cells, it is lowered to fit and a warning is shown.

I was a bit unsure about one point. In the code you pass seed to the constructor, but in the package generate(seed) calls random.seed(seed) only when seed > 0. So a seed of 0 gives a random maze on every run. If that's the behavior you want, you could add that sentence to the "Seed & levels" bullet. Check it against your own tests firs

# Team Organization & Methodology

Although our team did not use formal project management software like Jira or Trello, we adopted a highly structured Agile-inspired, communication-centric approach. 

## 1. Methodology
* **Verbal Synchronization:** Daily continuous oral communication replaced traditional ticketing. Decisions on architecture, feature priority, and bug fixing were made collectively in real-time.
* **Feature Branching:** Every feature, bug fix, or refactor was developed on an isolated Git branch.
* **Peer-Review Policy:** No code was pushed directly to the `main` branch. A strict cross-review policy was enforced: the author of a Pull Request could not merge their own code. The other team member was required to review, approve, and merge it. This resulted in exactly 28 rigorously reviewed PRs.

## 2. Task Distribution

**Cédric Henrotel (`cedrichenrotel`)**
* **Core Logic & Setup:** Project bootstrap, `main` entry point, and `config.json` parser (handling comments and validation) (PR #1, #2).
* **Game Entities:** Integration of the `mazegenerator` package, initialization of maze elements (Pac-Man, ghosts, pac-gums, super pac-gums), and building the `Entity` class hierarchy (`Pacman`, `Ghost`) using polymorphism (PR #2, #5).
* **Gameplay & Interactions:** Pac-Man movement, key bindings, sprite animations, pac-gum/super pac-gum logic, ghost vulnerability (blue ghosts), timer, and eating/respawning mechanics (flashing, death sprite) (PR #9, #12, #16, #18).
* **Display & UI:** Maze and elements rendering, resolution handling, cheat codes and their on-screen display, level timers, Win/Game Over screens with waiting time and blinking display (PR #8, #22, #26).
* **Refactoring & Fixes:** Project restructuring (`level.py` refactor, `draw` module), debugging (ghost movement, duplicate removal), maze size safety, and fixes on the new pac-gum system (reset on life loss, countdown, linting) (PR #20, #29, #30, #32).

**Mateo Gibert (`matgiber`)**
* **Architecture & Core Engine:** MiniLibX setup, `Game` / scene architecture, folder structure split (`engine` / `render`), level logic, and `GameEngine` class (PR #4, #6).
* **UI & Menus:** Main menu (selector, logo, colors, error messages), HUD (lives display on canvas), instructions page, pause menu, and player name input page (PR #4, #13, #14, #17, #21, #24).
* **AI, Pathfinding & Logic:** Ghost pathfinding algorithm (DFS), fleeing ghosts algorithm, level win detection, and collision detection (Pac-Man vs. ghosts) (PR #7, #13, #23).
* **Data Persistence:** Highscore system (`highscore.json` persistence, score recording, and display) (PR #10, #17, #25).
* **Optimization, Packaging & Support:** Rendering and game-loop optimization, window close handling, launch file, build/export command (`pyinstaller`), and macOS/Linux `mlx` support in `pyproject.toml` (PR #21, #24, #25).
* **Documentation & Refactoring:** README writing, refactoring of positioning, ghost side bug fix, and the new pac-gum system with a limit based on maze size (timer paused during pause menu) (PR #27, #28, #31, #32).

**Shared Responsibilities:**
* Code reviews on every Pull Request.
* Linting and typing compliance (`flake8`, `mypy`, `ruff`).
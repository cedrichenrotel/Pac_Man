# Project Timeline & Progress Tracking

Because we used a continuous verbal communication approach, we tracked our progress directly through our Git branches and Pull Requests rather than a traditional Gantt chart. The project naturally progressed through four main chronological phases.

## Phase 1: Foundation (PR #1 - #7)
* **Goal:** Establish the project architecture and basic rendering capabilities.
* **Progress:** Successfully bootstrapped the `main` entry point, integrated MiniLibX, and established the fundamental folder structure (`engine` vs. `render`). Basic maze generation and the base entity classes were implemented.

## Phase 2: Core Gameplay (PR #8 - #18)
* **Goal:** Implement player movement, enemy AI, and core game rules.
* **Progress:** Ghost pathfinding was initialized. Pac-Man's movement, collisions, and pac-gum logic were fully integrated. The highscore persistence system was also established during this phase.

## Phase 3: Polish & Menus (PR #20 - #27)
* **Goal:** Wrap the core gameplay loop in a complete user experience.
* **Progress:** Added the Pause menu, Instructions, and Highscore displays. Implemented Win/Loss screens. Significant work was done on rendering optimizations and setting up the final build packaging (`pyinstaller`).

## Phase 4: QA & Debugging (PR #28 - #32)
* **Goal:** Resolve edge cases, optimize performance, and ensure code quality.
* **Progress:** Optimized the pathfinding logic to prevent lag, fixed a ghost positioning bug, adjusted pac-gum limits dynamically based on maze size, and enforced strict linting/typing compliance across the entire codebase.
import sys
from collections import deque

from src.colors import COLORS

try:
    from mazegenerator import MazeGenerator

    from src.engine.utils import DIRECTIONS
except ImportError as e:
    print(f"{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}")
    sys.exit()


class Pathfinding:
    def __init__(self, maze: MazeGenerator):
        self.maze = maze
        self.visited: list[tuple[int, int]] = []
        self.real_path: list[tuple[int, int]] = []

    def can_move(self, direction: str, pos: tuple[int, int]) -> bool:
        """Check if it is possible to move in a direction."""

        dx, dy, code = DIRECTIONS[direction]

        if self.maze.maze[pos[1]][pos[0]] & code == 0:
            next_pos = (pos[0] + dx, pos[1] + dy)

            if next_pos not in self.visited:
                return True

        return False

    def move(self, direction: str, pos: tuple[int, int]) -> tuple[int, int]:
        """Move from a position in a direction."""

        dx, dy, code = DIRECTIONS[direction]

        return pos[0] + dx, pos[1] + dy

    def bfs(
        self, pos_pacman: tuple[int, int], pos_ghost: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        Find the shortest path from ghost to Pacman.
        """

        self.visited.clear()
        self.real_path.clear()

        queue = deque([pos_ghost])

        parent: dict[tuple[int, int], tuple[int, int] | None] = {
            pos_ghost: None
        }

        self.visited.append(pos_ghost)

        while queue:
            current = queue.popleft()

            if current == pos_pacman:
                break

            for direction in ["S", "N", "E", "W"]:
                if not self.can_move(direction, current):
                    continue

                next_pos = self.move(direction, current)

                self.visited.append(next_pos)

                parent[next_pos] = current

                queue.append(next_pos)

        if pos_pacman not in parent:
            raise RuntimeError("Pathfinding: no path found to pacman")

        path_node: tuple[int, int] | None = pos_pacman

        while path_node is not None:
            self.real_path.append(path_node)
            path_node = parent[path_node]

        self.real_path.reverse()

        return self.real_path[1:]

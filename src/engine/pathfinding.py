import sys
from src.colors import COLORS
try:
    from mazegenerator import MazeGenerator
    import random
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class Pathfinding():
    def __init__(self, maze: MazeGenerator):
        self.maze = maze

    def can_move(self, direction: str, pos: tuple[int, int],
                 visited: list[tuple[int, int]]) -> bool:
        """ check from position, direction N,S,E,W can be possible and
        also if its not allready been visited """

        directions: dict[str, tuple[int, int, int]] = {
            'N': (0, -1, 1),
            'E': (1, 0, 2),
            'S': (0, 1, 4),
            'W': (-1, 0, 8)
        }

        dx, dy, code = directions[direction]

        if self.maze.maze[pos[1]][pos[0]] & code == 0:
            next_pos = (pos[0] + dx, pos[1] + dy)
            if (next_pos not in visited):
                return True
        return False

    def move(self, direction: str, pos: tuple[int, int]) -> tuple[int, int]:
        """ move from a position to a direction """

        directions: dict[str, tuple[int, int, int]] = {
            'N': (0, -1, 1),
            'E': (1, 0, 2),
            'S': (0, 1, 4),
            'W': (-1, 0, 8)
        }

        dx, dy, code = directions[direction]
        next_pos = (pos[0] + dx, pos[1] + dy)
        return next_pos

    def get_free_paths(self, pos: tuple[int, int],
                       visited: list[tuple[int, int]]) -> list[str]:
        """ get all the possible coordinate from pos"""

        coordinates = ["S", "N", "E", "W"]
        coordinates_available = []
        for coordinate in coordinates:
            if self.can_move(coordinate, pos, visited) is True:
                coordinates_available.append(coordinate)
        return coordinates_available

    def return_where_possibility(
        self, pos: tuple[int, int], visited: list[tuple[int, int]]
    ) -> tuple[tuple[int, int] | None, list[str]]:
        """ get all the possible coordinate if pos is in dead end"""

        for visit in reversed(visited):
            new_pos = self.get_free_paths(visit, visited)
            if len(new_pos) != 0:
                return visit, new_pos
        return None, []

    def check_neighbour(
        self, pos: tuple[int, int], visited: list[tuple[int, int]],
        real_path: list[tuple[int, int]]
    ) -> tuple[tuple[int, int] | None, str | None]:
        """ choose neighbour cell from actual position """

        coordinates = self.get_free_paths(pos, visited)
        if len(coordinates) != 0:
            return pos, random.choice(coordinates)

        base_pos, coordinates = self.return_where_possibility(pos, visited)
        if base_pos is None:
            return None, None

        index_to = real_path.index(pos)
        index_from = real_path.index(base_pos)
        del real_path[index_from+1:index_to]
        del real_path[-1]

        return base_pos, random.choice(coordinates)

    def select_way(self, pos: tuple[int, int],
                   visited: list[tuple[int, int]],
                   real_path: list[tuple[int, int]]
                   ) -> tuple[int, int] | None:
        """ move and update position """

        base_pos, neigbour = self.check_neighbour(pos, visited, real_path)
        if base_pos is None or neigbour is None:
            return None
        actual_pos = self.move(neigbour, base_pos)
        visited.append(actual_pos)
        real_path.append(actual_pos)
        return actual_pos

    def bfs(self, pos_pacman: tuple[int, int],
            pos_ghost: tuple[int, int]) -> list[tuple[int, int]]:
        """ launchn the bfs algo and return the path
        from the ghost position to pacman position """

        visited = [pos_ghost]
        actual_pos = pos_ghost
        real_path: list[tuple[int, int]] = []

        while actual_pos != pos_pacman:
            next_pos = self.select_way(actual_pos, visited, real_path)
            if next_pos is None:
                raise RuntimeError("Pathfinding: no path found to pacman")
            actual_pos = next_pos
        print(real_path)
        return real_path

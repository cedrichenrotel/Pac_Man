import sys
from src.colors import COLORS
try:
    from mazegenerator import MazeGenerator
    from src.engine.pathfinding import Pathfinding
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class Entities():

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def move(self, direction: str, maze: MazeGenerator) -> bool:
        """ allows entities to move through the maze without
            passing through walls """

        directions: dict[str, tuple[int, int, int]] = {
            'N': (0, -1, 1),
            'E': (1, 0, 2),
            'S': (0, 1, 4),
            'W': (-1, 0, 8)
        }

        dx, dy, code = directions[direction]

        if maze.maze[self.y][self.x] & code == 0:
            self.x += dx
            self.y += dy
            return True
        return False


class Pacman(Entities):

    def __init__(self, x: int, y: int, lives: int) -> None:
        super().__init__(x, y)
        self.lives: int = lives


class Ghost(Entities):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.eaten: bool = False  # mangé
        self.is_edible: bool = False  # est comestible

    def moving_position_initial(self, maze: MazeGenerator) -> bool:
        """ change ghost position next to super_pacgum """

        directions = ["N", "S", "E", "W"]
        for direction in directions:
            if (self.move(direction, maze) is True):
                return True
        return False

    def path_to_pacman(self, maze: MazeGenerator, pacman: Pacman):
        """ get the path from ghost to pacman  """
        pos_pacman: tuple = (pacman.x, pacman.y)
        pos_ghost: tuple = (self.x, self.y)

        algo = Pathfinding(maze)
        algo.bfs(pos_pacman, pos_ghost)

import sys
from src.colors import COLORS
from src.engine.utils import DIRECTIONS
try:
    from mazegenerator import MazeGenerator
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

        dx, dy, code = DIRECTIONS[direction]

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

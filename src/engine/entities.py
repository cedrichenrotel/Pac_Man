import sys
from src.colors import COLORS
from src.engine.utils import DIRECTIONS, algo_fixed_walk
try:
    from mazegenerator import MazeGenerator
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class Entities():

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.render_x: float = x
        self.render_y: float = y

    def move(self, direction: str, maze: MazeGenerator) -> bool:
        """ allows entities to move through the maze without
            passing through walls """

        dx, dy, code = DIRECTIONS[direction]

        if maze.maze[self.y][self.x] & code == 0:
            self.x += dx
            self.y += dy
            return True
        return False

    def move_render(self) -> None:
        """ Smooth movement via the fixed pitch """

        algo_fixed_walk(self.render_x, self.x)
        algo_fixed_walk(self.render_y, self.y)


class Pacman(Entities):

    def __init__(self, x: int, y: int, lives: int) -> None:
        super().__init__(x, y)
        self.lives: int = lives


class Ghost(Entities):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.eaten: bool = False  # mangé
        self.is_edible: bool = False  # est comestible

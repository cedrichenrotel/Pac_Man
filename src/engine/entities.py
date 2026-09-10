import sys
from src.colors import COLORS
from src.engine.utils import DIRECTIONS, algo_fixed_walk
try:
    from mazegenerator import MazeGenerator
    from src.engine.pathfinding import Pathfinding
    from time import time
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class Entities():

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.render_x: float = x
        self.render_y: float = y
        self.key_direction: str | None = None
        self.current_pos: tuple[int, int] = (self.x, self.y)

    def move(self, direction: str, maze: MazeGenerator) -> bool:
        """ allows entities to move through the maze without
            passing through walls """

        dx, dy, code = DIRECTIONS[direction]
        if maze.maze[self.y][self.x] & code == 0:
            if self.render_x == self.x and self.render_y == self.y:
                self.current_pos = (self.x, self.y)
                self.x += dx
                self.y += dy
                return True
        return False

    def move_render(self, vitesse: float) -> bool:
        """ Smooth movement via the fixed pitch """
        stock_render_x: float = self.render_x
        stock_render_y: float = self.render_y

        self.render_x = algo_fixed_walk(self.render_x, self.x, vitesse)
        self.render_y = algo_fixed_walk(self.render_y, self.y, vitesse)

        if (self.render_x != stock_render_x or
           self.render_y != stock_render_y):
            return True
        return False


class Pacman(Entities):

    def __init__(self, x: int, y: int, lives: int) -> None:
        super().__init__(x, y)
        self.lives: int = lives
        self.frame_index: int = 0

    def decrease_life(self) -> None:
        self.lives -= 1


class Ghost(Entities):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.eaten: bool = False  # mangé
        self.is_edible: bool = False  # est comestible
        self.path_to_goal: list[str] = []
        self.frame_index: int = 0
        self.start_time_is_edible: int = None

    def time_is_edible(self) -> None:
        """ Vulnerability window for ghosts """

        if self.is_edible:
            vulnerability_time: int = time() - self.start_time_is_edible
            if vulnerability_time >= 5.00:
                self.is_edible = False

    def moving_position_initial(self, maze: MazeGenerator) -> bool:
        """ change ghost position next to super_pacgum """

        directions = ["N", "S", "E", "W"]
        for direction in directions:
            if (self.move(direction, maze) is True):
                self.render_x = self.x
                self.render_y = self.y
                return True
        return False

    def path_to_pacman(self, maze: MazeGenerator,
                       pacman: Pacman) -> list[tuple[int, int]]:
        """ get the path from ghost to pacman  """
        pos_pacman: tuple[int, int] = (pacman.x, pacman.y)
        pos_ghost: tuple[int, int] = (self.x, self.y)

        algo = Pathfinding(maze)
        return [pos_ghost] + algo.bfs(pos_pacman, pos_ghost)

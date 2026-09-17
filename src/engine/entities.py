import sys
from src.colors import COLORS
from src.engine.utils import DIRECTIONS, algo_fixed_walk
try:
    from mazegenerator import MazeGenerator
    from src.engine.pathfinding import Pathfinding
    from time import time
    from src.render.utils import transform_all_coord_to_cardinal
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
        self.frame_index: int = 0
        self.last_time: float = time()
        self.anim_last_time: float = 0.0

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

        dt: float = time() - self.last_time
        self.last_time = time()
        step: float = vitesse * dt
        self.anim_last_time += dt
        stock_render_x: float = self.render_x
        stock_render_y: float = self.render_y
        self.render_x = algo_fixed_walk(self.render_x, self.x, step)
        self.render_y = algo_fixed_walk(self.render_y, self.y, step)
        if self.anim_last_time >= 0.15:
            self.frame_index += 1
            self.anim_last_time = 0.0

        if self.render_x == self.x and self.render_y == self.y:
            self.current_pos = (self.x, self.y)

        if (self.render_x != stock_render_x or
           self.render_y != stock_render_y):
            return True
        return False


class Pacman(Entities):

    def __init__(self, x: int, y: int, lives: int) -> None:
        super().__init__(x, y)
        self.lives: int = lives
        self.dead: bool = False
        self.time_dead: float | None = None

    def decrease_life(self) -> None:

        if self.lives == 0:
            if self.time_dead is not None:
                elapsed_time: float = time() - self.time_dead
                elapsed_time // 0.15
            self.frame_index = 0
        else:
            self.lives -= 1


class Ghost(Entities):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.eaten: bool = False
        self.is_edible: bool = False
        self.path_to_goal: list[str] = []
        self.start_time_is_edible: float | None = None
        self.start_pos: tuple[int, int] = (x, y)
        self.time_edible = 10
        self.last_path_time: float = time()

    def time_is_edible(self, maze: MazeGenerator,
                       pacman: Pacman) -> float | None:
        """ Vulnerability window for ghosts """

        if self.is_edible:
            self.path_to_goal = transform_all_coord_to_cardinal(
                self.path_to_pacman(maze,
                                    pacman, True))
            assert self.start_time_is_edible is not None
            elapsed_time: float = time() - self.start_time_is_edible
            if elapsed_time >= self.time_edible:
                self.is_edible = False
                self.eaten = False
                self.path_to_goal = []
            return elapsed_time
        return None

    def init_ghost_eaten(self) -> None:
        """ resets the ghost to its original position """

        if self.eaten is True:
            self.current_pos = self.start_pos
            self.x, self.y = self.start_pos
            self.render_x, self.render_y = self.start_pos
            self.path_to_goal = []
            self.eaten = False

    def moving_position_initial(self, maze: MazeGenerator) -> bool:
        """ change ghost position next to super_pacgum """

        directions = ["N", "S", "E", "W"]
        for direction in directions:
            if (self.move(direction, maze) is True):
                self.render_x = self.x
                self.render_y = self.y
                return True
        return False

    def random_pos_away_from_pacman(self,
                                    pacman_pos: tuple[int, int],
                                    maze: 'MazeGenerator') -> tuple[int, int]:
        """get the oposite position (x,y) from pacman position"""
        oposite_x = 0
        dist_x_oposite = 0
        oposite_y = 0
        dist_y_oposite = 0
        for x in range(len(maze.maze)):
            for y in range(len(maze.maze[x])):

                if maze.maze[y][x] == 42:
                    continue
                dist_x = abs(pacman_pos[0] - x)
                dist_y = abs(pacman_pos[1] - y)

                if (dist_x > oposite_x):
                    oposite_x = dist_x
                    dist_x_oposite = x
                if (dist_y > oposite_y):
                    oposite_y = dist_y
                    dist_y_oposite = y

        return (dist_x_oposite, dist_y_oposite)

    def path_to_pacman(self, maze: MazeGenerator,
                       pacman: Pacman,
                       is_flee: bool = False) -> list[tuple[int, int]]:
        """ get the path from ghost to pacman  """
        pos_pacman: tuple[int, int] = (pacman.x, pacman.y)
        pos_ghost: tuple[int, int] = (self.x, self.y)

        algo = Pathfinding(maze)

        if is_flee is True:
            oposite = self.random_pos_away_from_pacman(pos_pacman, maze)
            return [pos_ghost] + algo.bfs(oposite, pos_ghost)
        else:
            return [pos_ghost] + algo.bfs(pos_pacman, pos_ghost)

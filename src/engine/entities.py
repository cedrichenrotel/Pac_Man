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
        self.frame_index: int = 0
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
        self.eaten: bool = False  # mangé
        self.is_edible: bool = False  # est comestible
        self.path_to_goal: list[str] = []
        self.frame_index: int = 0
        self.start_time_is_edible: float | None = None
        self.start_pos: tuple[int, int] = (x, y)
        self.time_edible = 10

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
                                    maze: list) -> tuple[int, int]:
        print(maze.maze)
        print(f"nb de ligne {len(maze.maze)}")
        print(f"nb de col {len(maze.maze[0])}")
        print(pacman_pos)

        # donc dans pacman pos de 0 a pacgum_pos et pacman_pos a 15
        # qu'elle est le plus grande ordre de grandeur

        magnitude_before_x = pacman_pos[0]
        magnitude_after_x = len(maze.maze[0])

        print(f"mag1 {magnitude_before_x}")
        print(f"mag2 {magnitude_after_x}")

        if magnitude_after_x > magnitude_before_x:
            oposite_x = len(maze.maze[0])
        else:
            oposite_x = pacman_pos[0]

        print(f"exact opposer: {oposite_x}")



        # magnitude_before_y = pacman_pos[1]
        # magnitude_after_y = len(maze.maze)


        # le plus eloigner de la pos du pacman
        # et si cest le milieu choise une
        # des quatres position eloigner en random

        # 1 exact opposer de la ou est pacman
        # 2 dans le maze
        # 3 pas dans 42
        # 4 retour en tuple x y
        pass

    def path_to_pacman(self, maze: MazeGenerator,
                       pacman: Pacman,
                       is_flee: bool = False) -> list[tuple[int, int]]:
        """ get the path from ghost to pacman  """
        # import random
        pos_pacman: tuple[int, int] = (pacman.x, pacman.y)
        pos_ghost: tuple[int, int] = (self.x, self.y)

        algo = Pathfinding(maze)

        if is_flee is True:
            # random_pos = (random.randint(0, maze._width-1),
            #               random.randint(0, maze._height-1))
            # is_valided = False
            self.random_pos_away_from_pacman(pos_pacman, maze)
            # while is_valided is not True:
            #     # if (maze.maze[random_pos[0]][random_pos[1]]):
            #     #     is_valided = True
            #     # else:
            #         random_pos = (random.randint(0, maze._width-1),
            #                       random.randint(0, maze._height-1))
            return [pos_ghost] + algo.bfs((0, 1), pos_ghost)
        else:
            return [pos_ghost] + algo.bfs(pos_pacman, pos_ghost)

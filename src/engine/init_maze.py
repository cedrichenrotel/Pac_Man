import sys
from src.colors import COLORS
try:
    import random
    from src.engine.utils import get_corners, get_center_maze
    from src.engine.model import Config_json
    from mazegenerator import MazeGenerator
    from src.error import GameError
    from src.engine.entities import Pacman, Ghost
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class InitMaze:
    """ combining the Labyrinth class and the configuration
       data to initialise the GameRender """

    def __init__(self, maze: MazeGenerator, config: Config_json) -> None:

        self.pacgum_pos: list[tuple[int, int]] = []
        self.superpacgum_pos: list[tuple[int, int]] = []
        self.maze: MazeGenerator = maze
        self.config: Config_json = config
        self.reserved_pos: list[tuple[int, int]] = []
        self.pacman: Pacman | None = None
        self.ghosts: list[Ghost] = []
        self.corners: dict[str, tuple[int, int]] = get_corners(self.maze)

    def init_pacgum(self) -> None:
        """ initialises the pagums in the maze at random and stores
            their positions in a list """

        nb_pacgum: int = self.config.pacgum
        lst_pos_val: list[tuple[int, int]] = []

        for y, line in enumerate(self.maze.maze):
            for x, val in enumerate(line):
                if (val != 15 and (x, y) not in self.reserved_pos):
                    lst_pos_val.append((x, y))

        if (nb_pacgum > len(lst_pos_val)):
            nb_pacgum = len(lst_pos_val)
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "Number of pacgum too high, using default")

        self.pacgum_pos = random.sample(lst_pos_val, nb_pacgum)

    def init_superpacgum(self) -> None:
        """ Initialising the superpacgum on the maze """

        for x, y in self.corners.values():
            self.superpacgum_pos.append((x, y))

    def init_pacman(self) -> None:
        """ Initialising the pacman on the maze """

        x, y = get_center_maze(self.maze)
        self.reserved_pos.append((x, y))
        self.pacman = Pacman(x, y, self.config.lives)

    def init_ghost(self) -> None:
        """ Initialising the ghost on the maze """

        self.reserved_pos.extend(self.corners.values())
        for x, y in self.corners.values():
            self.ghosts.append(Ghost(x, y))

        for ghost in self.ghosts:
            if (ghost.moving_position_initial(self.maze) is False):
                raise GameError("Error initializing the ghost")
            # ghost.path_to_pacman(self.maze, self.pacman)
        # # test:
        if self.pacman is not None:
            self.ghosts[0].path_to_pacman(self.maze, self.pacman)

    def config_start(self) -> None:
        """Initialising all the elements in the maze using separate
            functions """

        self.init_pacman()
        self.init_superpacgum()
        self.init_ghost()
        self.init_pacgum()

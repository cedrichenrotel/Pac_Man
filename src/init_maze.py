import sys
try:
    import random
    from src.error import ParseError
    from src.model import Config_json
    from mazegenerator import MazeGenerator
    from src.entities import Pacman, Ghost
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()


class RenderMaze:
    """ combining the Labyrinth class and the configuration
       data to initialise the game """

    def __init__(self, maze: MazeGenerator, config: Config_json) -> None:

        self.pacgum_pos: list[tuple[int, int]] = []
        self.maze: MazeGenerator = maze
        self.config: Config_json = config
        self.reserved_pos: list[tuple[int, int]] = []
        self.pacman: Pacman | None = None
        self.ghosts: list[Ghost] = []

    def init_pacgum(self) -> bool:
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
            print("[WARNING] Number of pacgum too high, using default")

        self.pacgum_pos = random.sample(lst_pos_val, nb_pacgum)
        return True

    def init_pacman(self) -> bool:
        """ Initialising the pacman on the maze """

        x, y = self.maze.maze_entry
        self.reserved_pos.append(self.maze.maze_entry)
        self.pacman = Pacman(x, y, self.config.lives)
        return True

    def init_ghost(self) -> bool:
        """ Initialising the ghost on the maze """

        height: int = len(self.maze.maze) - 1
        width: int = len(self.maze.maze[0]) - 1
        corner_maze: dict[str, tuple[int, int]] = {
         'top_left': (0, 0),
         'top_right': (width, 0),
         'low_left': (0, height),
         'low_right': (width, height)
        }

        self.reserved_pos.extend(corner_maze.values())

        for x, y in corner_maze.values():
            self.ghosts.append(Ghost(x, y))

        return True

    def config_start(self) -> bool:
        """Initialising all the elements in the maze using separate
            functions """

        if not self.init_pacman():
            raise ParseError("Config_start() -> Init_pacman initialisation "
                             "failed")

        if not self.init_ghost():
            raise ParseError("Config_start() -> Init_ghost initialisation "
                             "failed")

        if not self.init_pacgum():
            raise ParseError("Config_start() -> Init_pacgum initialisation "
                             "failed")
        return True

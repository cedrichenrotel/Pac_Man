import sys
try:
    import random
    from src.utils import get_corners
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
        self.superpacgum_pos: list[tuple[int, int]] = []
        self.maze: MazeGenerator = maze
        self.config: Config_json = config
        self.reserved_pos: list[tuple[int, int]] = []
        self.pacman: Pacman | None = None
        self.ghosts: list[Ghost] = []
        self.corners: dict[str, tuple[int, int]] = get_corners(self.maze)

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

    def init_superpacgum(self) -> bool:
        """ Initialising the superpacgum on the maze """

        for x, y in self.corners.values():
            self.superpacgum_pos.append((x, y))
        return True

    def init_pacman(self) -> bool:
        """ Initialising the pacman on the maze """

        x, y = self.maze.maze_entry
        self.reserved_pos.append(self.maze.maze_entry)
        self.pacman = Pacman(x, y, self.config.lives)
        return True

    def init_ghost(self) -> bool:
        """ Initialising the ghost on the maze """

        self.reserved_pos.extend(self.corners.values())

        for x, y in self.corners.values():
            self.ghosts.append(Ghost(x, y))

        return True

    def config_start(self) -> bool:
        """Initialising all the elements in the maze using separate
            functions """

        if not self.init_pacman():
            raise ParseError("Config_start() -> Init_pacman initialisation "
                             "failed")

        if not self.init_superpacgum():
            raise ParseError("Config_start() -> Init_superpacgum "
                             "initialisation failed")

        if not self.init_ghost():
            raise ParseError("Config_start() -> Init_ghost initialisation "
                             "failed")

        if not self.init_pacgum():
            raise ParseError("Config_start() -> Init_pacgum initialisation "
                             "failed")
        return True

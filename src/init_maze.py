import sys
from src.utils import COLORS
try:
    import random
    from src.error import ParseError
    from src.model import Config_json
    from mazegenerator import MazeGenerator
    # from src.entities import
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class RenderMaze:
    """ combining the Labyrinth class and the configuration
       data to initialise the game """

    def __init__(self, maze: MazeGenerator, config: Config_json) -> None:

        self.maze: MazeGenerator = maze
        self.config: Config_json = config
        self.pacgum_pos: list[tuple[int, int]] = []
        self.reserved_pos: list[tuple[int, int]] = []

    def config_start(self) -> int:

        if not self.init_pacgum():
            raise ParseError("Config_start() -> Pacgum initialisation failed")

    def init_pacgum(self) -> int:
        """ initialises the pagums in the maze at random and stores
            their positions in a list """

        nb_pacgum: int = self.config.pacgum
        pos_start: tuple[int, int] = self.maze.maze_entry
        lst_pos_val: list[tuple[int, int]] = []

        for y, line in enumerate(self.maze.maze):
            for x, val in enumerate(line):
                if (val != 15 and (x, y) != pos_start and
                   (x, y) not in self.reserved_pos):
                    lst_pos_val.append((x, y))

        if (nb_pacgum > len(lst_pos_val)):
            nb_pacgum = len(lst_pos_val)
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} Number of pacgum too high, using default")

        self.pacgum_pos = random.sample(lst_pos_val, nb_pacgum)
        return 1

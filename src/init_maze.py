import sys
try:
    import random
    from src.error import ParseError
    from src.model import Config_json
    from mazegenerator import MazeGenerator
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()


class RenderMaze:
    """ combining the Labyrinth class and the configuration
       data to initialise the game """

    def __init__(self, maze: MazeGenerator, config: Config_json) -> None:

        self.maze: MazeGenerator = maze
        self.config: Config_json = config
        self.pacgum_pos: list[tuple[int, int]] = []

    def config_start(self) -> int:

        if not self.init_pacgum():
            raise ParseError("Config_start() -> Pacgum initialisation failed")

    def init_pacgum(self) -> int:
        """ initialises the pagums in the maze at random and stores
            their positions in a list """

        pos_start: tuple[int, int] = self.maze.maze_entry
        lst_pos_val: list[tuple[int, int]] = []

        for y, line in enumerate(self.maze.maze):
            for x, val in enumerate(line):
                if val != 15 and (x, y) != pos_start:
                    lst_pos_val.append((x, y))

        if (self.config.pacgum > len(lst_pos_val)):
            raise ParseError("Init_pacgum() -> The pagum count is too large "
                             "relative to the valid position list")
        self.pacgum_pos = random.sample(lst_pos_val, self.config.pacgum)
        return 1

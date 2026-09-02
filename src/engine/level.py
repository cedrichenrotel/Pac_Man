import sys
from src.colors import COLORS

try:
    import os
    import json
    from pathlib import Path
    from src.engine.parse_config import parse_highscore
    from src.engine.load_config import create_json_missing
    from mazegenerator import MazeGenerator
    from src.engine.model import Config_json
    from src.engine.init_maze import InitMaze
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class Level():
    """ tracks level progression and score, and regenerates the maze
        when the player advances to the next level """

    def __init__(self, config: Config_json) -> None:
        self.config = config
        self.score: int = 0
        self.lvl_max: int = 10
        self.actual_lvl: int = 0
        self.highscore: dict[str, int]

    def generate_maze(self, seed: int) -> None:
        """ generates a maze for the given seed and initialises its
            elements """
        self.generator: MazeGenerator = MazeGenerator(
                    size=(self.config.level.width, self.config.level.height),
                    seed=seed
                    )

        self.init_maze: InitMaze = InitMaze(self.generator, self.config)
        self.init_maze.config_start()

    def add_score(self, num: int) -> None:
        self.score += num

    def next_level(self) -> None:
        """ called by the render side when the current level is won,
            regenerates the maze and reinitialises its elements """
        self.actual_lvl += 1
        self.generate_maze(self.config.seed + self.actual_lvl)

    def install_score(self) -> None:
        """ create highscore.json if missing otherwise
        parse the json """

        path = "./highscore.json"
        file = Path(path)
        if create_json_missing(file) is True:
            highscore = parse_highscore(file, path)
            if highscore is False:
                os.remove(path)
                create_json_missing(file)
            else:
                with open(path) as f:
                    self.highscore = json.load(f)
                # self.highscore = highscore
                print(self.highscore)

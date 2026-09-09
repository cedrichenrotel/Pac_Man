import sys
from src.colors import COLORS

try:
    from src.engine.utils import order_asc_and_limit
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
        self.player_name: str
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

    def push_new_score(self, path: str, highscore: dict[str, int]) -> None:
        """ push the new score from player to all highscore,
            order by descending, max 10 best score and write
            in highscore.json
        """

        new_score = {self.player_name: self.score}
        highscore.update(new_score)
        order_asc_and_limit(highscore)

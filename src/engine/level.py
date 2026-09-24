import sys

from src.colors import COLORS

try:
    from mazegenerator import MazeGenerator

    from src.engine.init_maze import InitMaze
    from src.engine.model import Config_json
    from src.engine.utils import order_asc_and_limit
except ImportError as e:
    print(f"{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}")
    sys.exit()


class Level:
    """tracks level progression and score, and regenerates the maze
    when the player advances to the next level"""

    def __init__(self, config: Config_json) -> None:
        self.config = config
        self.score: int = 0
        self.player_name: str = ""
        self.lvl_max: int = 10
        self.actual_lvl: int = 0
        self.highscore: dict[str, int]

    def generate_maze(self, seed: int) -> None:
        """generates a maze for the given seed and initialises its
        elements"""

        self.generator: MazeGenerator = MazeGenerator(
            size=(self.config.level.width, self.config.level.height), seed=seed
        )

        self.init_maze: InitMaze = InitMaze(self.generator, self.config)
        self.init_maze.config_start()

    def add_player_name(self, player_name: str) -> bool:
        self.player_name = player_name

        if player_name in self.highscore:
            return False
        return True

    def add_score(self, num: int) -> None:
        self.score += num

    def push_new_score(self, highscore: dict[str, int]) -> None:
        """push the new score from player to all highscore,
        order by descending, max 10 best score and write
        in highscore.json
        """
        if len(self.player_name) != 0:
            if self.player_name in self.highscore:
                if (
                    self.highscore[self.player_name] is None
                    or self.highscore[self.player_name] < self.score
                ):
                    self.highscore[self.player_name] = self.score
            else:
                self.new_score = {self.player_name: self.score}
                highscore.update(self.new_score)
            order_asc_and_limit(
                highscore,
                self.config.highscore_filename,
                self.player_name,
            )

    def save_score(
        self,
        player_name: str,
        score: int,
        highscore: dict[str, int],
    ) -> None:
        """save score and player at the end of a game"""

        self.highscore = highscore

        self.add_score(score)
        self.add_player_name(player_name)
        self.push_new_score(highscore)

    def next_level(self) -> None:
        """called by the render side when the current level is won,
        regenerates the maze and reinitialises its elements"""

        self.actual_lvl += 1
        self.generate_maze(self.config.seed + self.actual_lvl)

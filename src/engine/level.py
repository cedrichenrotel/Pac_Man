import sys
from src.colors import COLORS

try:
    import json
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
        new_score = {self.player_name: self.score}
        highscore.update(new_score)
        highscore = {k: v for k, v in
                     sorted(highscore.items(),
                            key=lambda item: item[1], reverse=True)}
        highscore = dict(list(highscore.items())[:10])
        try:
            with open(path, "w", encoding="utf-8"):
                pass
            with open(path, "w", encoding="utf-8") as f:
                json.dump(highscore, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  f"cannot push new scores in highscores: {e}")

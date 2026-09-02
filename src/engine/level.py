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

    # peut etre la mettre dans utils car je vais en avoir besoin
    # au moment de l'affichage des score
    def install_score_system(self) -> None:
        """ create highscore.json if missing otherwise
        parse the json """

        self.path = "./highscore.json"
        self.file = Path(self.path)
        if create_json_missing(self.file) is True:
            highscore = parse_highscore(self.file, self.path)
            if highscore is False:
                os.remove(self.path)
                create_json_missing(self.file)
            else:
                with open(self.path) as f:
                    self.highscore = json.load(f)
                print(self.highscore)

    def push_new_score(self) -> None:
        new_score = {self.player_name: self.score}
        self.highscore.update(new_score)
        self.highscore = {k: v for k, v in
                          sorted(self.highscore.items(),
                                 key=lambda item: item[1], reverse=True)}
        try:
            with open(self.path, "w", encoding="utf-8"):
                pass
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.highscore, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  f"cannot push new scores in highscores: {e}")

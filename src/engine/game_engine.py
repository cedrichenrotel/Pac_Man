import sys
from src.colors import COLORS
try:
    from src.engine.model import Config_json
    # from src.engine.level import Level
    from src.engine.init_maze import InitMaze
    from src.render.game import GameRender
    from mazegenerator import MazeGenerator
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class GameEngine():
    def __init__(self, config: Config_json):
        self.config = config

    def initialize(self):
        self.generator = MazeGenerator(
                    size=(self.config.level.width, self.config.level.height),
                    seed=self.config.seed
                    )
    
        self.init_maze: InitMaze = InitMaze(self.generator, self.config)
        self.init_maze.config_start()
        self.game_render = GameRender(1000, 1000)
        self.game_render.run()

    def run(self):
        self.initialize()
import sys
from src.colors import COLORS
try:
    from src.engine.model import Config_json
    from src.engine.level import Level
    from src.engine.init_maze import InitMaze
    from src.render.game import GameRender
    from mazegenerator import MazeGenerator
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class GameEngine():
    """ orchestrates the game lifecycle: maze generation, maze
        initialisation, level tracking and launching the render """

    def __init__(self, config: Config_json) -> None:
        self.config: Config_json = config

    def generate_maze(self, seed: int) -> None:
        """ generates a maze for the given seed and initialises its
            elements """
        self.generator: MazeGenerator = MazeGenerator(
                    size=(self.config.level.width, self.config.level.height),
                    seed=seed
                    )

        self.init_maze: InitMaze = InitMaze(self.generator, self.config)
        self.init_maze.config_start()

    def initialize(self) -> None:
        """ generates the first maze, initialises its elements and
            launches the render """

        self.generate_maze(self.config.seed)
        self.level: Level = Level(self)
        self.game_render: GameRender = GameRender(1000, 1000, self)
        self.game_render.run()

    def run(self) -> None:
        """ entry point of the engine """

        self.initialize()

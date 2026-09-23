import sys

from src.colors import COLORS

try:
    from pathlib import Path

    from src.engine.model import Config_json
    from src.engine.utils import install_score_system
    from src.render.game import GameRender
    from src.render.utils import (
        HUD_BOTTOM_HEIGHT,
        HUD_TOP_HEIGHT,
    )
except ImportError as e:
    print(f"{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}")
    sys.exit()


CELL_SIZE_PX: int = 56


class GameEngine:
    """orchestrates the game lifecycle: maze generation, maze
    initialisation, level tracking and launching the render"""

    def __init__(self, config: Config_json) -> None:
        self.config: Config_json = config
        self.path = config.highscore_filename
        self.file = Path(self.path)

    def initialize(self) -> None:
        """generates the first maze, initialises its elements and
        launches the render"""

        width = self.config.level.width * CELL_SIZE_PX
        height = (
            self.config.level.height * CELL_SIZE_PX
            + HUD_TOP_HEIGHT
            + HUD_BOTTOM_HEIGHT
        )
        self.highscore = install_score_system(self.path, self.file)
        self.game_render: GameRender = GameRender(
            width, height, self, self.config, self.highscore
        )
        self.game_render.run()

    def run(self) -> None:
        """entry point of the engine"""

        self.initialize()

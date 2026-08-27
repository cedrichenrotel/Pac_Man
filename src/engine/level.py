import sys
from src.colors import COLORS

try:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from src.engine.game_engine import GameEngine
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


class Level():
    """ tracks level progression and score, and regenerates the maze
        when the player advances to the next level """

    def __init__(self, game_engine: "GameEngine") -> None:
        self.game_engine: "GameEngine" = game_engine
        self.score: int = 0
        self.lvl_max: int = 10
        self.actual_lvl: int = 0

    def add_score(self, num: int) -> None:
        self.score += num

    def next_level(self) -> None:
        """ called by the render side when the current level is won,
            regenerates the maze and reinitialises its elements """
        self.actual_lvl += 1
        self.game_engine.generate_maze(
            self.game_engine.config.seed + self.actual_lvl)

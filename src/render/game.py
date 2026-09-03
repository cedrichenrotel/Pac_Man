from typing import Optional, Union, TYPE_CHECKING
from src.render.scenes.menu import MenuScene
from src.render.scenes.level import LevelScene
from src.render.scenes.score import ScoreScene
from src.engine.model import Config_json
from src.render.scenes.instruction import InstructionScene
from mlx import Mlx
from src.error import GameError

SceneType = Union[MenuScene, LevelScene, ScoreScene, InstructionScene]

if TYPE_CHECKING:
    from src.engine.game_engine import GameEngine


class GameRender():
    '''Class GameRender on contaim the basics for launch
    the GameRender and the size of the screen'''
    def __init__(self, width: int, height: int,
                 game_engine: "GameEngine",
                 config: Config_json,
                 highscore: dict[str, int]) -> None:
        self.highscore = highscore
        self.config = config
        self.game_engine = game_engine
        self.width: int = width
        self.height: int = height
        self.running: bool = True
        self.mlx: Mlx = Mlx()

    def run(self) -> None:
        """launch mlx threw the menu scene"""
        self.mlx_init: Optional[int] = self.mlx.mlx_init()
        if self.mlx_init is None:
            raise GameError("Cannot init properly the mlx")
        self.mlx_window: Optional[int] = self.mlx.mlx_new_window(
            self.mlx_init, self.width, self.height, "Pac-Man")
        if self.mlx_window is None:
            raise GameError("Cannot init properly the window of mlx")

        self.current_scene: SceneType = MenuScene(self, self.mlx,
                                                  self.mlx_init,
                                                  self.mlx_window,
                                                  self.width,
                                                  self.height,
                                                  self.config,
                                                  self.highscore)
        self.current_scene.launch()
        self.mlx.mlx_loop(self.mlx_init)
        self.mlx.mlx_release(self.mlx_init)

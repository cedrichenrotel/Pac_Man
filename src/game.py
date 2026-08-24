from typing import Optional, Union
from src.scenes.menu import MenuScene
from src.scenes.level import LevelScene
from src.scenes.score import ScoreScene
from src.scenes.instruction import InstructionScene
from mlx import Mlx
# import time

SceneType = Union[MenuScene, LevelScene, ScoreScene, InstructionScene]


class Game():
    '''Class Game on contaim the basics for launch
    the game and the size of the screen'''
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.running: bool = True
        self.mlx: Mlx = Mlx()

    def run(self) -> None:
        """launch mlx threw the menu scene"""
        self.mlx_init: Optional[int] = self.mlx.mlx_init()
        if self.mlx_init is None:
            return
        self.mlx_window: Optional[int] = self.mlx.mlx_new_window(
            self.mlx_init, self.width, self.height, "Pac-Man")
        if self.mlx_window is None:
            return
        self.current_scene: SceneType = MenuScene(self, self.mlx,
                                                  self.mlx_init,
                                                  self.mlx_window,
                                                  self.width,
                                                  self.height)
        self.current_scene.launch()
        self.mlx.mlx_loop(self.mlx_init)
        self.mlx.mlx_release(self.mlx_init)

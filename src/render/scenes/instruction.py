from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import XK_ESCAPE, install_menu_image
from mlx import Mlx
from src.engine.model import Config_json


# guarded to avoid a circular import: GameRender.py imports InstructionScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class InstructionScene:
    def __init__(self, GameRender: "GameRender", mlx: Mlx,
                 mlx_init: Optional[int],
                 mlx_window: Optional[int],
                 width: int,
                 height: int,
                 config: Config_json,
                 highscore: dict[str, int],
                 player_name: str,
                 score: int) -> None:
        self.player_name = player_name
        self.highscore = highscore
        self.config = config
        self.GameRender = GameRender
        self.width = width
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window
        self.score = score

    def launch(self) -> None:
        '''display the instructions scene'''
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        assert self.mlx_init is not None and self.mlx_window is not None
        self.img = install_menu_image("./assets/instruction/rules.png",
                                      self.mlx, self.mlx_init, self.mlx_window,
                                      self.width, self.height)
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

    def on_key(self, keycode: int, param: object) -> None:
        '''go back to the menu scene on escape'''

        if keycode == XK_ESCAPE:
            from src.render.scenes.menu import MenuScene
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height,
                self.config, self.highscore, self.player_name,
                self.score)
            self.GameRender.current_scene.launch()

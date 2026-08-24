from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.utils import YELLOW, LIGHT_GRAY, XK_ESCAPE
from mlx import Mlx

# guarded to avoid a circular import: game.py imports LevelScene at module
# level, so Game can only be imported here for type hints
if TYPE_CHECKING:
    from src.game import Game


class LevelScene:
    def __init__(self, game: "Game", mlx: Mlx, mlx_init: Optional[int],
                 mlx_window: Optional[int], width: int, height: int) -> None:
        self.game = game
        self.width = width
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window

    def launch(self) -> None:
        '''display the level scene'''
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                int(self.width / 2) - 100,
                                int(self.height / 2),
                                YELLOW, "Level (TODO)")
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                int(self.width / 2) - 100,
                                int(self.height / 2) + 40,
                                LIGHT_GRAY, "Press ESC to return to menu")
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

    def on_key(self, keycode: int, param: object) -> None:
        '''go back to the menu scene on escape'''
        if keycode == XK_ESCAPE:
            from src.scenes.menu import MenuScene
            self.game.current_scene = MenuScene(self.game, self.mlx,
                                                self.mlx_init,
                                                self.mlx_window,
                                                self.width, self.height)
            self.game.current_scene.launch()

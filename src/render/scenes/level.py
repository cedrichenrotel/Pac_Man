from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import YELLOW, LIGHT_GRAY, XK_ESCAPE
from mlx import Mlx

# guarded to avoid a circular import: GameRender.py imports LevelScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class LevelScene:
    def __init__(self, GameRender: "GameRender", mlx: Mlx,
                 mlx_init: Optional[int],
                 mlx_window: Optional[int], width: int, height: int) -> None:
        self.GameRender = GameRender
        self.width = width
        self.score = 0
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
            from src.render.scenes.menu import MenuScene
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height)
            self.GameRender.current_scene.launch()

    def winning(self) -> None:
        # example de si le lvl etait gagner
        lvl_engine = self.GameRender.game_engine.level
        if (lvl_engine.actual_lvl != lvl_engine.lvl_max):
            lvl_engine.add_score(self.score)
            lvl_engine.next_level()
            # ducoup apres next_level redessiner limage du maze
        else:
            # si jamais le nombre de level max etait atteind, on reviens
            # au menu. egalement on devrait plus tard ajouter le score
            # au highscore
            from src.render.scenes.menu import MenuScene
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height)
            self.GameRender.current_scene.launch()

from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import YELLOW, LIGHT_GRAY, XK_ESCAPE
from mlx import Mlx
from src.engine.model import Config_json
from src.engine.level import Level
# guarded to avoid a circular import: GameRender.py imports LevelScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class LevelScene:
    def __init__(self, GameRender: "GameRender", mlx: Mlx,
                 mlx_init: Optional[int],
                 mlx_window: Optional[int],
                 width: int,
                 height: int,
                 config: Config_json) -> None:
        self.config = config
        self.GameRender = GameRender
        self.width = width
        self.score = 0
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window

    def launch(self) -> None:
        '''display the level scene'''
        self.level_engine: Level = Level(self.config)
        self.level_engine.generate_maze(self.config.seed)
        self.level_engine.install_score_system()

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
                self.width, self.height, self.config)
            self.GameRender.current_scene.launch()

    def winning(self) -> None:
        # example de si le lvl etait gagner
        self.level_engine.push_new_score()
        if (self.level_engine.actual_lvl != self.level_engine.lvl_max):
            self.level_engine.add_score(self.score)
            self.level_engine.next_level()
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
                self.width, self.height, self.config)
            self.GameRender.current_scene.launch()

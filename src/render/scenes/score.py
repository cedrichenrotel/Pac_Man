from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import YELLOW, LIGHT_GRAY, XK_ESCAPE
from src.engine.model import Config_json
from mlx import Mlx
import time

# guarded to avoid a circular import: GameRender.py imports ScoreScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class ScoreScene:
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

    # def show_highscores(self) -> None:
    #     self.marge = 0
    #     if self.highscore is not None:
    #         time.sleep(1000 / 1_000_000.0)
    #         for key, value in self.highscore.items():
    #             time.sleep(1000 / 1_000_000.0)
    #             self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
    #                                     int(self.width / 2) - 100,
    #                                     int(self.height / 4) + self.marge,
    #                                     YELLOW, f"{key}: {value}")            
    #             self.marge += 40

    #     time.sleep(3000 / 1_000_000.0)

    def show_highscores(self) -> None:
        self.marge = 0
        if self.highscore is not None:
            max_y = self.height - 80  # laisser de la place pour le message ESC
            for key, value in self.highscore.items():
                y = int(self.height / 4) + self.marge
                if y > max_y:
                    break  # ou réduire l'espacement / passer en scroll
                self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                        int(self.width / 2) - 100,
                                        y, YELLOW, f"{key}: {value}")
                self.marge += 40

    def launch(self) -> None:
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.mlx.mlx_loop_hook(self.mlx_init, self.redraw, self)
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

    def redraw(self, param: object = None) -> None:
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.show_highscores()
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                int(self.width / 2) - 100,
                                int(self.height / 4) + self.marge + 40,
                                LIGHT_GRAY, "Press ESC to return to menu")

    # def launch(self) -> None:
    #     '''display the level scene'''

    #     self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
    #     self.show_highscores()

    #     self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
    #                             int(self.width / 2) - 100,
    #                             int(self.height / 4) + self.marge + 40,
    #                             LIGHT_GRAY, "Press ESC to return to menu")
    #     self.mlx.mlx_do_sync(self.mlx_init)
    #     self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

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

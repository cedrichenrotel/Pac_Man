from __future__ import annotations

from typing import TYPE_CHECKING

from mlx import Mlx

from src.engine.level import Level
from src.engine.model import Config_json
from src.render.utils import XK_RETURN, YELLOW

# guarded to avoid a circular import: GameRender.py imports ScoreScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class Winner:
    def __init__(
        self,
        GameRender: GameRender,
        mlx: Mlx,
        mlx_init: int | None,
        mlx_window: int | None,
        width: int,
        height: int,
        config: Config_json,
        highscore: dict[str, int],
        player_name: str,
        score: int,
    ) -> None:
        self.score: int = score
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
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.mlx.mlx_loop_hook(self.mlx_init, self.redraw, self)
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

    def redraw(self, param: object = None) -> None:
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)

        list_text: list[str] = [
            "YOU WIN!",
            f"Final score: {self.score}",
            "Press ENTER to continue",
        ]

        step: int = 40
        for i, text in enumerate(list_text):
            y = self.height // 4 + step * i
            self.mlx.mlx_string_put(
                self.mlx_init,
                self.mlx_window,
                int(self.width / 2) - 100,
                y,
                YELLOW,
                text,
            )

    def on_key(self, keycode: int, param: object) -> None:
        """go back to the menu scene on escape"""

        if keycode == XK_RETURN:
            if len(self.player_name) != 0:
                level_engine = Level(self.config)
                level_engine.save_score(
                    self.player_name, self.score, "./highscore", self.highscore
                )
                from src.render.scenes.menu import MenuScene

                self.GameRender.current_scene = MenuScene(
                    self.GameRender,
                    self.mlx,
                    self.mlx_init,
                    self.mlx_window,
                    self.width,
                    self.height,
                    self.config,
                    self.highscore,
                    self.player_name,
                    self.score,
                )
                self.GameRender.current_scene.launch()
            else:
                from src.render.scenes.player import PlayerScene

                player = PlayerScene(
                    self.GameRender,
                    self.mlx,
                    self.mlx_init,
                    self.mlx_window,
                    self.width,
                    self.height,
                    self.config,
                    self.highscore,
                    self.player_name,
                    self.score,
                )
                player.launch()

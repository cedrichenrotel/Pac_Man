from __future__ import annotations

from typing import Any

from src.engine.level import Level
from src.render.utils import XK_RETURN, YELLOW


class Winner:
    def __init__(self, game: Any) -> None:
        self.game = game
        self.score: int = self.game.score
        self.player_name = self.game.player_name
        self.highscore = self.game.highscore
        self.config = self.game.config
        self.GameRender = self.game.GameRender
        self.width = self.game.width
        self.height = self.game.height
        self.mlx = self.game.mlx
        self.mlx_init = self.game.mlx_init
        self.mlx_window = self.game.mlx_window
        self.score = self.game.score

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

                self.GameRender.current_scene = MenuScene(self)
                self.GameRender.current_scene.launch()
            else:
                from src.render.scenes.player import PlayerScene

                player = PlayerScene(self)
                player.launch()

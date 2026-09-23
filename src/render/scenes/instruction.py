from __future__ import annotations

from typing import Any

from src.render.utils import XK_ESCAPE, install_menu_image


class InstructionScene:
    def __init__(self, game: Any) -> None:
        self.game = game
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
        """display the instructions scene"""
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        assert self.mlx_init is not None and self.mlx_window is not None
        self.img = install_menu_image(
            "./assets/instruction/rules.png",
            self.mlx,
            self.mlx_init,
            self.mlx_window,
            self.width,
            self.height,
        )
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

    def on_key(self, keycode: int, param: object) -> None:
        """go back to the menu scene on escape"""

        if keycode == XK_ESCAPE:
            from src.render.scenes.menu import MenuScene

            self.GameRender.current_scene = MenuScene(self)
            self.GameRender.current_scene.launch()

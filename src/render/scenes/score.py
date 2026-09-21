from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import LIGHT_GRAY, XK_ESCAPE
from src.engine.model import Config_json
from src.render.utils import pil_to_mlx_image
from mlx import Mlx

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

    def draw_score_on_canvas(self) -> None:
        """Display on HUD of high score"""
        from PIL import ImageDraw, ImageFont, Image

        hud_height = 400
        hud_canvas = Image.new("RGBA", (self.width, hud_height),
                               (0, 0, 0, 255))
        draw = ImageDraw.Draw(hud_canvas)

        try:
            font = ImageFont.load_default(size=22)
        except TypeError:
            font = ImageFont.load_default()

        self.marge = 0
        if self.highscore is not None:
            for key, value in self.highscore.items():
                score = f"{key}: {value}"
                draw.text((self.width // 2 - 70, self.marge),
                          score, fill=(255, 255, 0, 255), font=font)
                self.marge += 40

        hud_ptr: int = pil_to_mlx_image(hud_canvas, "score.png",
                                        self.mlx_init, self.mlx)
        self.mlx.mlx_put_image_to_window(self.mlx_init, self.mlx_window,
                                         hud_ptr, 0, 200)

    def launch(self) -> None:
        '''display the level scene'''

        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.draw_score_on_canvas()
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                int(self.width / 2) - 100,
                                int(self.height / 4) + self.marge + 40,
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
                self.width, self.height,
                self.config, self.highscore, self.player_name,
                self.score)
            self.GameRender.current_scene.launch()

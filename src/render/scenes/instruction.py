from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import XK_ESCAPE
from mlx import Mlx
from src.engine.model import Config_json
from PIL import Image
import os


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
                 highscore: dict[str, int]) -> None:
        self.highscore = highscore
        self.config = config
        self.GameRender = GameRender
        self.width = width
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window

    def launch(self) -> None:
        '''display the instructions scene'''

        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "./../../../"
                                               "assets/instruction/rules.png")
        image_path = os.path.normpath(image_path)
        Image.open(image_path).convert("RGBA").save(image_path)

        self.img = self.mlx.mlx_png_file_to_image(
            self.mlx_init, image_path)
        img_ptr, img_width, img_height = self.img

        x = self.width - img_width
        y = self.height - img_height

        if img_ptr:
            self.mlx.mlx_put_image_to_window(self.mlx_init, self.mlx_window,
                                             img_ptr, int(x / 2),
                                             int(y / 2))

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
                self.config, self.highscore)
            self.GameRender.current_scene.launch()

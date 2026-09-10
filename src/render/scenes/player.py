from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from mlx import Mlx
from src.render.scenes.menu import MenuScene
from src.render.utils import (XK_RETURN, list_key, RED, XK_BACK,
                              clear_rect)
from src.engine.model import Config_json
import os
from PIL import Image

# guarded to avoid a circular import: GameRender.py imports InstructionScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class PlayerScene:
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
        self.player_name = ""

    def launch(self) -> None:
        '''display the instructions scene'''

        self.mlx.mlx_loop_hook(self.mlx_init, None, self)
        self.middle_w: int = int(self.width / 2) - 100
        self.middle_h: int = int(self.height / 2) - 100
        self.name_x: int = self.middle_w + 35
        self.name_y: int = self.middle_h + 120
        self.install_menu_image()
        self.mlx.mlx_do_sync(self.mlx_init)
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

    def clear_name(self) -> None:
        '''erase only the typed name, instead of clearing and
        redrawing the whole scene on every keystroke'''

        assert self.mlx_init is not None and self.mlx_window is not None
        clear_rect(self.mlx, self.mlx_init, self.mlx_window,
                   self.name_x, self.name_y, 150, 20)

    def delete_letter(self) -> None:
        """delete the last letter"""

        if len(self.player_name) > 0:
            self.player_name = self.player_name[:-1]
            self.clear_name()
            self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                    self.name_x, self.name_y,
                                    RED, self.player_name)

    def install_menu_image(self) -> None:
        '''install in the scene an image from assets/'''

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "./../../../"
                                               "assets/player/who_i_am.png")
        image_path = os.path.normpath(image_path)
        Image.open(image_path).convert("RGBA").save(image_path)

        self.img = self.mlx.mlx_png_file_to_image(
            self.mlx_init, image_path)
        img_ptr, img_width, img_height = self.img

        x = self.width - img_width
        y = self.height - img_height

        if img_ptr:
            self.mlx.mlx_put_image_to_window(self.mlx_init, self.mlx_window,
                                             img_ptr, int(x / 2), int(y / 2))

    def write_letter(self, key: str) -> None:
        """write name with the new letter"""

        if (len(self.player_name) < 10):
            self.player_name += key
            self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                    self.name_x, self.name_y,
                                    RED, self.player_name)

    def on_key(self, keycode: int, param: object) -> None:
        '''write and delete on recording
        keyboard and accept enter to go menu'''

        record = [item for item in list_key if item[0] == keycode]
        if len(record) > 0:
            self.write_letter(record[0][1])
        if keycode == XK_RETURN:
            if (len(self.player_name) > 2):
                self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
                self.GameRender.current_scene = MenuScene(
                    self.GameRender, self.mlx,
                    self.mlx_init,
                    self.mlx_window,
                    self.width, self.height,
                    self.config, self.highscore)
                self.GameRender.current_scene.launch()
        if keycode == XK_BACK:
            self.delete_letter()

    def back_menu(self) -> None:
        '''go back to the menu scene'''

        from src.render.scenes.menu import MenuScene
        self.GameRender.current_scene = MenuScene(
            self.GameRender, self.mlx,
            self.mlx_init,
            self.mlx_window,
            self.width, self.height,
            self.config, self.highscore)
        self.GameRender.current_scene.launch()

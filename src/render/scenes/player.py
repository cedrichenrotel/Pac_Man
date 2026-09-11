from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from mlx import Mlx
from src.engine.level import Level
from src.render.scenes.menu import MenuScene
from src.render.utils import (XK_RETURN, list_key, RED, XK_BACK,
                              clear_rect, install_menu_image, YELLOW)
from src.engine.model import Config_json

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
                 highscore: dict[str, int],
                 player_name: str,
                 score: int) -> None:
        self.score = score
        self.highscore = highscore
        self.config = config
        self.GameRender = GameRender
        self.width = width
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window
        self.player_name = player_name

    def launch(self) -> None:
        '''display the instructions scene'''

        self.mlx.mlx_loop_hook(self.mlx_init, None, self)
        self.middle_w: int = int(self.width / 2) - 100
        self.middle_h: int = int(self.height / 2) - 100
        self.name_x: int = self.middle_w + 35
        self.name_y: int = self.middle_h + 120
        assert self.mlx_init is not None and self.mlx_window is not None
        self.img = install_menu_image("./assets/player/who_i_am.png",
                                      self.mlx, self.mlx_init, self.mlx_window,
                                      self.width, self.height)
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
                self.level_engine: Level = Level(self.config)
                self.level_engine.highscore = self.highscore
                if self.level_engine.add_player_name(self.player_name) is True:
                    self.level_engine.add_score(self.score)
                    self.level_engine.push_new_score("./highscore",
                                                     self.highscore)
                else:
                    self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                            int(self.width / 2),
                                            int(self.height / 2),
                                            YELLOW,
                                            "player allready "
                                            "exist cannot progress")
                    return
                self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
                self.GameRender.current_scene = MenuScene(
                    self.GameRender, self.mlx,
                    self.mlx_init,
                    self.mlx_window,
                    self.width, self.height,
                    self.config, self.highscore, self.player_name, self.score)

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
            self.config, self.highscore, self.player_name,
            self.score)
        self.GameRender.current_scene.launch()

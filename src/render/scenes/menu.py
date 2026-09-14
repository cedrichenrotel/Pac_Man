from __future__ import annotations
from typing import Callable, List, Optional, Tuple, TYPE_CHECKING
from src.render.scenes.level import LevelScene
from src.render.scenes.score import ScoreScene
from src.engine.model import Config_json
from src.render.scenes.instruction import InstructionScene
from src.render.utils import (YELLOW, LIGHT_GRAY, XK_UP, XK_DOWN,
                              XK_RETURN, install_menu_image)
from mlx import Mlx

# guarded to avoid a circular import: GameRender.py imports MenuScene at module
# level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class MenuScene:
    def __init__(self, GameRender: 'GameRender', mlx: Mlx,
                 mlx_init: Optional[int],
                 mlx_window: Optional[int],
                 width: int,
                 height: int,
                 config: Config_json,
                 highscore: dict[str, int],
                 player_name: str,
                 score: int) -> None:
        self.score = score
        self.player_name = player_name
        self.highscore = highscore
        self.config = config
        self.GameRender = GameRender
        self.width = width
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window
        self.selected: int = 0
        self.active: bool = True
        self.img: Tuple[Optional[int], int, int] = (0, 0, 0)
        self.entries: List[Tuple[str, Callable[[], None]]] = [
              ("Start GameRender", self.start_game),
              ("View Highscores", self.show_highscores),
              ("Instructions", self.show_instructions),
              ("Exit", self.quit_game),
          ]

    def get_calc(self) -> None:
        '''calcul to get the center of the screen'''

        self.middle_w: int = int(self.width / 2) - 100
        self.middle_h: int = int(self.height / 2) - 100
        self.step: int = 40

    def draw_selector(self, x: int, y: int) -> None:
        '''draw the selector '>' of menu'''

        height = 12
        for dy in range(-height // 2, height // 2 + 1):
            width = height // 2 - abs(dy)
            for dx in range(width):
                self.mlx.mlx_pixel_put(self.mlx_init, self.mlx_window,
                                       x + dx, y + dy, LIGHT_GRAY)

    def draw_menu(self) -> None:
        '''install the title with them redirections'''

        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        if self.img[0]:
            img_ptr, img_width, _ = self.img
            left_space = self.width - img_width
            self.mlx.mlx_put_image_to_window(self.mlx_init, self.mlx_window,
                                             img_ptr, int(left_space / 2), 0)
        for i, (label, _action) in enumerate(self.entries):
            y = self.middle_h + self.step * i
            if i == self.selected:
                self.draw_selector(self.middle_w - 20, y + 10)
            self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                    self.middle_w, y, YELLOW, label)

    def on_key(self, keycode: int, param: object) -> None:
        '''record the key press and do the action
        key up to go up, key down to go down,
        enter to select the title'''

        if not self.active:
            return
        if keycode == XK_UP:
            self.selected = (self.selected - 1) % len(self.entries)
            self.draw_menu()
        elif keycode == XK_DOWN:
            self.selected = (self.selected + 1) % len(self.entries)
            self.draw_menu()
        elif keycode == XK_RETURN:
            self.entries[self.selected][1]()

    def launch(self) -> None:
        self.get_calc()
        self.mlx.mlx_loop_hook(self.mlx_init, None, self)
        self.mlx.mlx_expose_hook(self.mlx_window, None, self)
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        assert self.mlx_init is not None and self.mlx_window is not None
        self.img = install_menu_image("./assets/menu/menu_logo.png",
                                      self.mlx, self.mlx_init, self.mlx_window,
                                      self.width, self.height, False)
        self.draw_menu()
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

    def start_game(self) -> None:
        '''redirect to the level scene'''

        if self.img[0]:
            self.mlx.mlx_destroy_image(self.mlx_init, self.img[0])
        self.active = False
        self.GameRender.current_scene = LevelScene(
            self.GameRender, self.mlx,
            self.mlx_init, self.mlx_window,
            self.width, self.height, self.config,
            self.highscore, self.player_name,
            self.score)
        self.GameRender.current_scene.launch()

    def show_highscores(self) -> None:
        '''redirect to the score scene'''

        if self.img[0]:
            self.mlx.mlx_destroy_image(self.mlx_init, self.img[0])
        self.active = False
        self.GameRender.current_scene = ScoreScene(
            self.GameRender, self.mlx,
            self.mlx_init, self.mlx_window,
            self.width, self.height, self.config,
            self.highscore, self.player_name, self.score)
        self.GameRender.current_scene.launch()

    def show_instructions(self) -> None:
        '''redirect to the instruction scene'''

        if self.img[0]:
            self.mlx.mlx_destroy_image(self.mlx_init, self.img[0])
        self.active = False
        self.GameRender.current_scene = InstructionScene(
            self.GameRender, self.mlx,
            self.mlx_init,
            self.mlx_window,
            self.width, self.height, self.config,
            self.highscore, self.player_name,
            self.score)
        self.GameRender.current_scene.launch()

    def quit_game(self) -> None:
        """mlx quitting the GameRender"""

        self.running = False
        self.mlx.mlx_loop_exit(self.mlx_init)

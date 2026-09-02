from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import (YELLOW, LIGHT_GRAY_PIX, XK_ESCAPE,
                              get_cell_size)
from src.engine.utils import DIRECTIONS
from src.engine.entities import Pacman
from mlx import Mlx

# guarded to avoid a circular import: GameRender.py imports LevelScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class LevelScene:

    def __init__(self, GameRender: "GameRender", mlx: Mlx,
                 mlx_init: Optional[int],
                 mlx_window: Optional[int], width: int, height: int) -> None:

        self.GameRender = GameRender
        self.maze = self.GameRender.game_engine.generator.maze
        self.width = width
        self.score = 0
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window
        self.maze_width: int = self.GameRender.game_engine.config.level.width
        self.maze_height: int = self.GameRender.game_engine.config.level.height

    def draw_wall(self, x: int, y: int) -> None:
        """allows the pixel size to be standardised and the walls of the maze
            to be displayed pixel by pixel"""

        cell_size: int = get_cell_size(self.width,
                                       self.height,
                                       self.maze_width,
                                       self.maze_height)
        val: int = self.maze[y][x]
        img_ptr, width, height = (self.GameRender.sprites_stores.
                                  sprites['wall'][0])

        for direction, (dx, dy, code) in DIRECTIONS.items():
            if val & code != 0:
                px: int = x * cell_size
                py: int = y * cell_size
                for i in range(0, cell_size, width):
                    if dx == 0:
                        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                                         self.mlx_window,
                                                         img_ptr,
                                                         px + i,
                                                         py + cell_size // 2 + dy * (cell_size // 2))

                    else:
                        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                                         self.mlx_window,
                                                         img_ptr,
                                                         px + cell_size // 2 + dx * (cell_size // 2),
                                                         py + i)

    def draw_maze(self) -> None:
        """ As you navigate the maze, the y and x coordinates are sent to
            `draw_wall` to display the walls """

        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                self.draw_wall(x, y)

    def on_expose(self, param: object) -> None:
        self.render()

    def render(self) -> None:

        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.draw_maze()
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                int(self.width / 2) - 100,
                                int(self.height / 2),
                                YELLOW, "Level (TODO)")
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                int(self.width / 2) - 100,
                                int(self.height / 2) + 40,
                                LIGHT_GRAY_PIX, "Press ESC to return to menu")
        self.draw_pacman()
        self.draw_pacgum()

    def launch(self) -> None:
        '''display the level scene'''

        self.render()
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)
        self.mlx.mlx_expose_hook(self.mlx_window, self.on_expose, self)

    def on_key(self, keycode: int, param: object) -> None:
        '''go back to the menu scene on escape'''
        if keycode == XK_ESCAPE:
            self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
            from src.render.scenes.menu import MenuScene
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height)
            self.GameRender.current_scene.launch()

    def winning(self) -> None:
        # example de si le lvl etait gagner
        lvl_engine = self.GameRender.game_engine.level
        if (lvl_engine.actual_lvl != lvl_engine.lvl_max):
            lvl_engine.add_score(self.score)
            self.maze = self.GameRender.game_engine.generator.maze
            lvl_engine.next_level()
            self.render()
        else:
            # si jamais le nombre de level max etait atteind, on reviens
            # au menu. egalement on devrait plus tard ajouter le score
            # au highscore
            from src.render.scenes.menu import MenuScene
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height)
            self.GameRender.current_scene.launch()

    def draw_pacman(self) -> None:
        """Draw the Pacman sprite on the maze."""

        pacman: Pacman = self.GameRender.game_engine.init_maze.pacman
        cell_size: int = get_cell_size(self.width,
                                       self.height,
                                       self.maze_width,
                                       self.maze_height)
        px: int = pacman.x * cell_size
        py: int = pacman.y * cell_size
        img_ptr, width, height = (self.GameRender.sprites_stores.
                                  sprites['pacman'][0])
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         img_ptr,
                                         px + cell_size // 2 ,
                                         py + cell_size // 2 )

    def draw_pacgum(self) -> None:
        """Draw the Pacgum sprite on the maze."""
        pacgums: list[tuple[int, int]] = (self.GameRender.game_engine.
                                        init_maze.pacgum_pos)
        cell_size: int = get_cell_size(self.width,
                                       self.height,
                                       self.maze_width,
                                       self.maze_height)
        for pacgum in pacgums:
            px: int = pacgum[0] * cell_size
            py: int = pacgum[1] * cell_size
            img_ptr, width, height = (self.GameRender.sprites_stores.
                                      sprites['pacgum'][0])
            self.mlx.mlx_put_image_to_window(self.mlx_init,
                                             self.mlx_window,
                                             img_ptr,
                                             px + cell_size // 2,
                                             py + cell_size // 2)
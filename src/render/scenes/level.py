from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import (YELLOW, LIGHT_GRAY_PIX, XK_ESCAPE,
                              get_cell_size)
from src.engine.utils import DIRECTIONS
from src.engine.entities import Ghost
from mlx import Mlx
from src.engine.model import Config_json
from src.engine.level import Level
# guarded to avoid a circular import: GameRender.py imports LevelScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class LevelScene:

    def __init__(self, GameRender: "GameRender", mlx: Mlx,
                 mlx_init: Optional[int],
                 mlx_window: Optional[int],
                 width: int,
                 height: int,
                 config: Config_json) -> None:
        self.config = config
        self.GameRender = GameRender
        self.width = width
        self.score = 0
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window
        self.maze_width: int = self.GameRender.game_engine.config.level.width
        self.maze_height: int = self.GameRender.game_engine.config.level.height

    def _grid(self) -> tuple[int, int, int]:
        """ cell size, snapped to a multiple of the wall sprite so tiling
            never overshoots a cell, plus the (x, y) margins that center
            the maze in the window given that snapping """

        _, wall_width, _ = self.GameRender.sprites_stores.sprites['wall'][0]
        reserve: int = wall_width // 2
        cell_size: int = get_cell_size(self.width,
                                       self.height,
                                       self.maze_width,
                                       self.maze_height,
                                       reserve,
                                       wall_width)
        margin_x: int = (self.width - self.maze_width * cell_size) // 2
        margin_y: int = (self.height - self.maze_height * cell_size) // 2
        return cell_size, margin_x, margin_y

    def draw_wall(self, x: int, y: int) -> None:
        """allows the pixel size to be standardised and the walls of the maze
            to be displayed pixel by pixel"""

        img_ptr, width, height = (self.GameRender.sprites_stores.
                                  sprites['wall'][0])
        cell_size, margin_x, margin_y = self._grid()
        val: int = self.maze[y][x]

        directions_to_draw = ['N', 'W']
        if x == self.maze_width - 1:
            directions_to_draw.append('E')
        if y == self.maze_height - 1:
            directions_to_draw.append('S')

        for direction in directions_to_draw:
            dx, dy, code = DIRECTIONS[direction]
            if val & code != 0:
                px: int = margin_x + x * cell_size
                py: int = margin_y + y * cell_size
                for i in range(0, cell_size, width):
                    if dx == 0:
                        if dy == -1:
                            py_pos: int = py - height // 2
                        else:
                            py_pos = py + cell_size - height // 2
                        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                                         self.mlx_window,
                                                         img_ptr,
                                                         px + i,
                                                         py_pos)
                    else:
                        if dx == -1:
                            px_pos: int = px - width // 2
                        else:
                            px_pos = px + cell_size - width // 2
                        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                                         self.mlx_window,
                                                         img_ptr,
                                                         px_pos,
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
        self.draw_maze()
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                int(self.width // 2) - 100,
                                int(self.height // 2),
                                YELLOW, "Level (TODO)")
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                int(self.width // 2) - 100,
                                int(self.height // 2) + 40,
                                LIGHT_GRAY_PIX, "Press ESC to return to menu")
        self.draw_pacman()
        self.draw_pacgum()
        self.draw_super_pacgum()
        self.draw_gosth()

    def launch(self) -> None:
        '''display the level scene'''

        self.level_engine: Level = Level(self.config)
        self.level_engine.generate_maze(self.config.seed)
        self.maze = self.level_engine.generator.maze

        self.render()
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)
        self.mlx.mlx_expose_hook(self.mlx_window, self.on_expose, self)
        # self.mlx.mlx_loop_hook(self.mlx_init, self.on_loop, self)

    def on_loop(self, param: object) -> None:
        """ est rappeler automatiquement par mlx_loop pour avancer
            render_x/y un pas vers x/y, dessine les positions intermediaure """

        ghosts: list[Ghost] = self.level_engine.init_maze.ghosts
        self.level_engine.init_maze.pacman.move_render()
        for ghost in ghosts:
            ghost.move_render()
        self.render()

    def on_key(self, keycode: int, param: object) -> None:
        '''go back to the menu scene on escape'''

        if keycode == XK_ESCAPE:
            self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
            from src.render.scenes.menu import MenuScene
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height, self.config)
            self.GameRender.current_scene.launch()

    def winning(self) -> None:
        # example de si le lvl etait gagner
        if (self.level_engine.actual_lvl != self.level_engine.lvl_max):
            self.level_engine.add_score(self.score)
            self.level_engine.next_level()
            self.maze = self.level_engine.generator.maze
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
                self.width, self.height, self.config)
            self.GameRender.current_scene.launch()

    def draw_pacman(self) -> None:
        """Draw the Pacman sprite on the maze."""

        pacman = self.level_engine.init_maze.pacman
        assert pacman is not None
        cell_size, margin_x, margin_y = self._grid()
        px: int = margin_x + pacman.x * cell_size
        py: int = margin_y + pacman.y * cell_size
        img_ptr, width, height = (self.GameRender.sprites_stores.
                                  sprites['pacman'][0])
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         img_ptr,
                                         px + cell_size // 2 - width // 2,
                                         py + cell_size // 2 - height // 2)

    def draw_gosth(self) -> None:

        ghosts: list[Ghost] = self.level_engine.init_maze.ghosts
        cell_size, margin_x, margin_y = self._grid()
        img_ptr, width, height = (self.GameRender.sprites_stores.
                                  sprites['ghost_red'][0])
        for ghost in ghosts:
            px: int = margin_x + ghost.x * cell_size
            py: int = margin_y + ghost.y * cell_size
            self.mlx.mlx_put_image_to_window(self.mlx_init,
                                             self.mlx_window,
                                             img_ptr,
                                             px + cell_size // 2 - width // 2,
                                             py + cell_size // 2 - height // 2)

    def draw_pacgum(self) -> None:
        """ Draw the Pacgum sprite on the maze. """
        pacgums: list[tuple[int, int]] = self.level_engine.init_maze.pacgum_pos
        cell_size, margin_x, margin_y = self._grid()
        for pacgum in pacgums:
            px: int = margin_x + pacgum[0] * cell_size
            py: int = margin_y + pacgum[1] * cell_size
            img_ptr, width, height = (self.GameRender.sprites_stores.
                                      sprites['pacgum'][0])
            self.mlx.mlx_put_image_to_window(self.mlx_init,
                                             self.mlx_window,
                                             img_ptr,
                                             px + cell_size // 2 - width // 2,
                                             py + cell_size // 2 - height // 2)

    def draw_super_pacgum(self) -> None:
        """ Draw the Super Pacgum sprite on the maze. """

        super_pacgums: list[tuple[int, int]] = (
            self.level_engine.init_maze.superpacgum_pos)
        cell_size, margin_x, margin_y = self._grid()
        for super_pacgum in super_pacgums:
            px: int = margin_x + super_pacgum[0] * cell_size
            py: int = margin_y + super_pacgum[1] * cell_size
            img_ptr, width, height = (self.GameRender.sprites_stores.
                                      sprites['super_pacgum'][0])
            self.mlx.mlx_put_image_to_window(self.mlx_init,
                                             self.mlx_window,
                                             img_ptr,
                                             px + cell_size // 2 - width // 2,
                                             py + cell_size // 2 - height // 2)

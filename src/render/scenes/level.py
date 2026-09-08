from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING
from src.render.utils import (XK_ESCAPE, XK_UP,
                              XK_DOWN, XK_LEFT,
                              XK_RIGHT, get_cell_size,
                              get_asset_path)
from src.engine.utils import DIRECTIONS
from src.engine.entities import Ghost, Pacman
from mlx import Mlx
from src.engine.model import Config_json
from src.engine.level import Level
from PIL import Image
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

    def _paste_wall_segment(self, x: int, y: int, dx: int, dy: int) -> None:

        wall_width, wall_height = self.wall_sprite.size
        cell_size, margin_x, margin_y = self._grid()

        px: int = margin_x + x * cell_size
        py: int = margin_y + y * cell_size
        for i in range(0, cell_size, wall_width):
            if dx == 0:
                if dy == -1:
                    py_pos: int = py - wall_height // 2
                else:
                    py_pos = py + cell_size - wall_height // 2
                self.canvas.paste(self.wall_sprite, (px + i, py_pos),
                                  self.wall_sprite)
            else:
                if dx == -1:
                    px_pos: int = px - wall_width // 2
                else:
                    px_pos = px + cell_size - wall_width // 2
                self.canvas.paste(self.wall_sprite,
                                  (px_pos, py + i),
                                  self.wall_sprite)

    def draw_wall(self, x: int, y: int) -> None:
        """allows the pixel size to be standardised and the walls of the maze
            to be displayed pixel by pixel"""

        val: int = self.maze[y][x]

        directions_to_draw: list[str] = ['N', 'W']
        if x == self.maze_width - 1:
            directions_to_draw.append('E')
        if y == self.maze_height - 1:
            directions_to_draw.append('S')

        for direction in directions_to_draw:
            dx, dy, code = DIRECTIONS[direction]
            if val & code != 0:
                self._paste_wall_segment(x, y, dx, dy)

    def draw_maze(self) -> bool:
        """ As you navigate the maze, the y and x coordinates are sent to
            `draw_wall` to display the walls """

        image_path: str = get_asset_path("sprites/wall/wall.png")
        self.wall_sprite = Image.open(image_path).convert("RGBA")
        self.canvas = Image.new("RGBA", (self.width, self.height),
                                (0, 0, 0, 0))

        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                self.draw_wall(x, y)
        if (self.draw_pacgum() is False or
           self.draw_super_pacgum() is False):
            return False
        os.makedirs(".cache", exist_ok=True)
        tmp_path: str = os.path.join(".cache", "maze_cache.png")
        self.canvas.save(tmp_path)
        self.maze_img_ptr, _, _ = self.mlx.mlx_png_file_to_image(self.mlx_init,
                                                                 tmp_path)
        return True

    def on_expose(self, param: object) -> None:
        self.render()

    def render(self) -> None:

        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         self.maze_img_ptr, 0, 0)
        self.draw_pacman()
        self.draw_ghost()

    def launch(self) -> None:
        '''display the level scene'''

        self.level_engine: Level = Level(self.config)
        self.level_engine.generate_maze(self.config.seed)
        self.maze = self.level_engine.generator.maze
        self.maze_width: int = self.level_engine.config.level.width
        self.maze_height: int = self.level_engine.config.level.height
        if self.draw_maze() is False:
            return
        self.render()
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)
        self.mlx.mlx_expose_hook(self.mlx_window, self.on_expose, self)
        self.mlx.mlx_loop_hook(self.mlx_init, self.on_loop, self)

    def on_loop(self, param: object) -> None:
        """ is automatically called by mlx_loop to move forward
            render_x/y moves one step in the x/y direction, drawing the
            intermediate positions """

        ghosts: list[Ghost] = self.level_engine.init_maze.ghosts
        pacman: Pacman | None = self.level_engine.init_maze.pacman
        assert pacman is not None

        if pacman.key_direction is not None:
            pacman.move(pacman.key_direction, self.level_engine.generator)
            pacman.frame_index += 1
            if pacman.move_render() is True:
                self.render()
        for ghost in ghosts:
            if ghost.move_render() is True:
                self.render()

    def on_key(self, keycode: int, param: object) -> None:
        '''go back to the menu scene on escape'''

        pacman: Pacman | None = self.level_engine.init_maze.pacman
        assert pacman is not None
        try:
            from src.render.scenes.menu import MenuScene
        except ImportError as e:
            print(f"[ERROR] level.py: {e}")
            return

        if keycode == XK_ESCAPE:
            self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height, self.config)
            self.GameRender.current_scene.launch()
        elif keycode == XK_UP:
            pacman.key_direction = 'N'
        elif keycode == XK_DOWN:
            pacman.key_direction = 'S'
        elif keycode == XK_LEFT:
            pacman.key_direction = 'W'
        elif keycode == XK_RIGHT:
            pacman.key_direction = 'E'

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

        pacman: Pacman | None = self.level_engine.init_maze.pacman
        assert pacman is not None
        cell_size, margin_x, margin_y = self._grid()
        px: int = int(margin_x + pacman.render_x * cell_size)
        py: int = int(margin_y + pacman.render_y * cell_size)
        direction_sprites: dict[str, str] = {
            'N': 'pacman_chomp_n',
            'S': 'pacman_chomp_s',
            'W': 'pacman_chomp_w',
            'E': 'pacman_chomp'
        }
        sprite_name: str = direction_sprites.get(pacman.key_direction or 'E',
                                                 'pacman_chomp')
        img_ptr, width, height = (self.GameRender.sprites_stores.
                                  sprites[sprite_name]
                                  [pacman.frame_index % 4])
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         img_ptr,
                                         px + cell_size // 2 - width // 2,
                                         py + cell_size // 2 - height // 2)

    def draw_ghost(self) -> None:

        ghosts: list[Ghost] = self.level_engine.init_maze.ghosts
        cell_size, margin_x, margin_y = self._grid()

        for ghost in ghosts:
            img_ptr, width, height = (self.GameRender.sprites_stores.
                                      sprites['ghost_red']
                                      [ghost.frame_index % 4])
            px: int = int(margin_x + ghost.render_x * cell_size)
            py: int = int(margin_y + ghost.render_y * cell_size)
            self.mlx.mlx_put_image_to_window(self.mlx_init,
                                             self.mlx_window,
                                             img_ptr,
                                             px + cell_size // 2 - width // 2,
                                             py + cell_size // 2 - height // 2)

    def draw_pacgum(self) -> bool:
        """ Draw the Pacgum sprite on the maze. """

        try:
            image_path: str = get_asset_path("sprites/pacgum/pacgum.png")
            self.pacgum_sprite = Image.open(image_path).convert("RGBA")
        except FileNotFoundError as e:
            from src.render.scenes.menu import MenuScene
            self.GameRender.current_scene = MenuScene(
                  self.GameRender, self.mlx,
                  self.mlx_init,
                  self.mlx_window,
                  self.width, self.height, self.config)
            self.GameRender.current_scene.launch()
            print(f"[ERROR] draw_pacgum: path error -> {e}")
            return False

        pacgum_width, pacgum_height = self.pacgum_sprite.size

        pacgums: list[tuple[int, int]] = self.level_engine.init_maze.pacgum_pos

        cell_size, margin_x, margin_y = self._grid()

        for pacgum in pacgums:
            px: int = margin_x + pacgum[0] * cell_size
            py: int = margin_y + pacgum[1] * cell_size
            self.canvas.paste(self.pacgum_sprite,
                              (px + cell_size // 2 - pacgum_width // 2,
                               py + cell_size // 2 - pacgum_height // 2),
                              self.pacgum_sprite)
        return True

    def draw_super_pacgum(self) -> bool:
        """ Draw the Super Pacgum sprite on the maze. """

        try:
            image_path: str = get_asset_path("sprites/pacgum/super_pacgum.png")
            self.super_pacgum_sprite = Image.open(image_path).convert("RGBA")
        except FileNotFoundError as e:
            from src.render.scenes.menu import MenuScene
            self.GameRender.current_scene = MenuScene(
                  self.GameRender, self.mlx,
                  self.mlx_init,
                  self.mlx_window,
                  self.width, self.height, self.config)
            self.GameRender.current_scene.launch()
            print(f"[ERROR] draw_super_pacgum: path error -> {e}")
            return False

        super_pacgum_width, super_pacgum_height = self.super_pacgum_sprite.size

        super_pacgums: list[tuple[int, int]] = (
            self.level_engine.init_maze.superpacgum_pos)

        cell_size, margin_x, margin_y = self._grid()

        for super_pacgum in super_pacgums:
            px: int = margin_x + super_pacgum[0] * cell_size
            py: int = margin_y + super_pacgum[1] * cell_size
            self.canvas.paste(self.super_pacgum_sprite,
                              (px + cell_size // 2 - super_pacgum_width // 2,
                               py + cell_size // 2 - super_pacgum_height // 2),
                              self.super_pacgum_sprite)
        return True

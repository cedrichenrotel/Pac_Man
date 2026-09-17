from __future__ import annotations
import os
from src.engine.entities import Ghost, Pacman
from src.engine.level import Level
from src.engine.utils import DIRECTIONS
from src.render.utils import get_cell_size, get_asset_path, YELLOW
from typing import Optional, Any
from mlx import Mlx
from PIL import Image
from time import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # noqa import: flake8 can't see the use below because the attribute
    # is named the same as the type (GameRender: GameRender)
    from src.render.game import GameRender  # noqa: F401


class Draw:

    mlx: Mlx
    mlx_init: Optional[int]
    mlx_window: Optional[int]
    maze: list[list[int]]
    maze_width: int
    maze_height: int
    GameRender: GameRender
    height: int
    width: int
    level_engine: Level
    pacman: Optional[Pacman]
    score: int
    cheat_freeze_ghost: bool
    cheat_invincible: bool
    move_pac: int

    def _put_sprite_centered(self, x: float, y: float, img_ptr: int,
                             height: int, width: int) -> None:
        """ centres the sprites in the middle of the tile """

        px: int = int(self.margin_x + x * self.cell_size)
        py: int = int(self.margin_y + y * self.cell_size)
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         img_ptr,
                                         px + self.cell_size // 2 - width // 2,
                                         py + self.cell_size // 2
                                         - height // 2)

    def _grid(self) -> tuple[int, int, int]:
        """ cell size, snapped to a multiple of the wall sprite so tiling
            never overshoots a cell, plus the (x, y) margins that center
            the maze in the window given that snapping """

        _, wall_width, _ = self.GameRender.sprites_stores.sprites['wall'][0]
        reserve: int = wall_width // 2
        self.cell_size: int = get_cell_size(self.width,
                                            self.height,
                                            self.maze_width,
                                            self.maze_height,
                                            reserve,
                                            wall_width)
        self.margin_x: int = (self.width - self.maze_width
                              * self.cell_size) // 2
        self.margin_y: int = (self.height - self.maze_height
                              * self.cell_size) // 2
        return self.cell_size, self.margin_x, self.margin_y

    def _paste_wall_segment(self, x: float, y: float, dx: int,
                            dy: int) -> None:

        wall_width, wall_height = self.wall_sprite.size

        px: int = int(self.margin_x + x * self.cell_size)
        py: int = int(self.margin_y + y * self.cell_size)
        for i in range(0, self.cell_size, wall_width):
            if dx == 0:
                if dy == -1:
                    py_pos: int = py - wall_height // 2
                else:
                    py_pos = py + self.cell_size - wall_height // 2
                self.canvas.paste(self.wall_sprite, (px + i, py_pos),
                                  self.wall_sprite)
            else:
                if dx == -1:
                    px_pos: int = px - wall_width // 2
                else:
                    px_pos = px + self.cell_size - wall_width // 2
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

        self.maze_img_ptr: int = self._pil_to_mlx_image(self.canvas,
                                                        "maze_cache.png")
        return True

    def draw_pacman(self) -> None:
        """Draw the Pacman sprite on the maze."""
        life = None
        if self.pacman is not None:
            life = self.pacman.lives
        self.pacman = self.level_engine.init_maze.pacman
        assert self.pacman is not None
        if life is not None:
            self.pacman.lives = life

        px: int = int(self.margin_x + self.pacman.render_x * self.cell_size)
        py: int = int(self.margin_y + self.pacman.render_y * self.cell_size)
        direction_sprites: dict[str, str] = {
            'N': 'pacman_chomp_n',
            'S': 'pacman_chomp_s',
            'W': 'pacman_chomp_w',
            'E': 'pacman_chomp'
        }
        sprite_name: str = direction_sprites.get(self.pacman.key_direction
                                                 or 'E', 'pacman_chomp')

        if self.pacman.lives == 0:
            if self.pacman.time_dead is None:
                self.pacman.time_dead = time()
            death_frame = int((time() - self.pacman.time_dead) // 0.15)
            img_ptr, width, height = (self.GameRender.sprites_stores.
                                      sprites['pacman_death']
                                      [death_frame % 7])
            if death_frame >= 7:
                self.pacman.dead = True
        else:
            img_ptr, width, height = (self.GameRender.sprites_stores.
                                      sprites[sprite_name]
                                      [self.pacman.frame_index % 4])
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         img_ptr,
                                         px + self.cell_size // 2 - width // 2,
                                         py + self.cell_size //
                                         2 - height // 2)

    def draw_ghost(self) -> None:
        """Draw the ghost sprite on the maze """

        self.ghosts: list[Ghost] = self.level_engine.init_maze.ghosts
        color_ghost: dict[str, str] = {
            'R': 'ghost_red',
            'B': 'ghost_blue'
        }

        for ghost in self.ghosts:
            sprite_ghost: str = ""
            if ghost.is_edible is False:
                sprite_ghost = color_ghost['R']
            elif ghost.is_edible is True:
                sprite_ghost = color_ghost['B']
                vulnerability_time: float | None = ghost.time_is_edible()
                assert vulnerability_time is not None
                flashing: int = int(vulnerability_time * 5)
                if (vulnerability_time >= 8 and
                   flashing % 2 == 0):
                    sprite_ghost = color_ghost['R']
            img_ptr, width, height = (self.GameRender.sprites_stores.
                                      sprites[sprite_ghost]
                                      [ghost.frame_index % 4])
            self._put_sprite_centered(ghost.render_x,
                                      ghost.render_y,
                                      img_ptr,
                                      height,
                                      width)

    def draw_pacgum(self) -> bool:
        """ Draw the Pacgum sprite on the maze. """

        img_ptr, width, height = (self.GameRender.sprites_stores.
                                  sprites['pacgum'][0])
        pacgums = self.level_engine.init_maze.pacgum_pos

        for pacgum in pacgums:
            self._put_sprite_centered(pacgum[0],
                                      pacgum[1],
                                      img_ptr,
                                      height,
                                      width)
        return True

    def draw_super_pacgum(self) -> bool:
        """ Draw the Super Pacgum sprite on the maze. """

        img_ptr, width, height = (self.GameRender.sprites_stores.
                                  sprites['super_pacgum'][0])

        super_pacgums: list[tuple[int, int]] = (
            self.level_engine.init_maze.superpacgum_pos)

        for super_pacgum in super_pacgums:
            self._put_sprite_centered(super_pacgum[0],
                                      super_pacgum[1],
                                      img_ptr,
                                      height,
                                      width)
        return True

    def show_life(self) -> None:
        assert self.pacman is not None
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                10,
                                self.height - 40,
                                YELLOW, f"life: {self.pacman.lives}")

    def show_score(self) -> None:
        """ display the score when Pac-Man eats the Pac-Gums during
            the current game """

        assert self.pacman is not None
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                self.width - 150,
                                self.height - 40,
                                YELLOW, f"score: {self.score}")

    def _pil_to_mlx_image(self, canvas: Image.Image, filename: str) -> Any:
        """ saves the image to a .cache folder if it does not exist, stores it
            on the hard drive and displays the image """

        os.makedirs(".cache", exist_ok=True)
        path = os.path.join(".cache", filename)
        canvas.save(path)
        ptr, _, _ = self.mlx.mlx_png_file_to_image(self.mlx_init, path)
        return ptr

    def draw_hud_on_canvas(self) -> None:
        """Display on HUD text with score and life"""
        from PIL import ImageDraw, ImageFont

        hud_height = 50
        hud_canvas = Image.new("RGBA", (self.width, hud_height),
                               (0, 0, 0, 255))
        draw = ImageDraw.Draw(hud_canvas)

        try:
            font = ImageFont.load_default(size=22)
        except TypeError:
            font = ImageFont.load_default()

        life_count = self.pacman.lives if self.pacman else 0
        text_life = f"LIFE: {life_count}"
        text_score = f"SCORE: {self.score}"

        draw.text((20, 12), text_life, fill=(255, 255, 0, 255), font=font)
        draw.text((self.width - 160, 12), text_score, fill=(255, 255, 0, 255),
                  font=font)

        hud_ptr: int = self._pil_to_mlx_image(hud_canvas, "hud_cache.png")
        self.mlx.mlx_put_image_to_window(self.mlx_init, self.mlx_window,
                                         hud_ptr, 0, self.height - hud_height)

    def draw_cheat(self) -> None:
        """ Display of cheat commands with on/off switch to check if active """

        from PIL import ImageDraw, ImageFont

        hud_height = 50
        hud_canvas = Image.new("RGBA", (self.width, hud_height),
                               (0, 0, 0, 255))
        draw = ImageDraw.Draw(hud_canvas)

        try:
            font = ImageFont.load_default(size=15)
        except TypeError:
            font = ImageFont.load_default()
        list_text: list[tuple[str, Any]] = [
            ("(W) FREEZE GHOST:  ", self.cheat_freeze_ghost),
            ("(Q) INVINCIBLE:  ", self.cheat_invincible),
            ("(T) SPEED MOVE:  ", self.move_pac != 3),
            ("(R) ADD LIFE POINT", None),
            ("(E) SKIP LEVEL", None)
        ]

        max_rows: int = 2
        for i, text in enumerate(list_text):
            row: int = i % max_rows
            col: int = i // max_rows
            x = 15 + col * 200
            y = 12 + row * 20

            label, state = text
            suffix = ('ON' if state else 'OFF') if state is not None else ''
            draw.text((x, y),
                      label + suffix,
                      fill=(255, 255, 0, 255),
                      font=font
                      )

        cheat_ptr: int = self._pil_to_mlx_image(hud_canvas, "cheat_cache.png")
        self.mlx.mlx_put_image_to_window(self.mlx_init, self.mlx_window,
                                         cheat_ptr, 0, 0)

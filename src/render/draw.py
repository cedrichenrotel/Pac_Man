from __future__ import annotations
import os
from src.engine.entities import Ghost, Pacman
from src.engine.utils import DIRECTIONS
from PIL import Image
from time import time
from src.render.utils import get_cell_size, get_asset_path


class Draw:

    def _put_sprite_centered(self, x: float, y: float, img_ptr: int,
                             height: int, width: int) -> None:
        """ centres the sprites in the middle of the tile """

        cell_size, margin_x, margin_y = self._grid()
        px: int = int(margin_x + x * cell_size)
        py: int = int(margin_y + y * cell_size)
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         img_ptr,
                                         px + cell_size // 2 - width // 2,
                                         py + cell_size // 2 - height // 2)

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

    def _paste_wall_segment(self, x: float, y: float, dx: int,
                            dy: int) -> None:

        wall_width, wall_height = self.wall_sprite.size
        cell_size, margin_x, margin_y = self._grid()

        px: int = int(margin_x + x * cell_size)
        py: int = int(margin_y + y * cell_size)
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
        os.makedirs(".cache", exist_ok=True)
        tmp_path: str = os.path.join(".cache", "maze_cache.png")
        self.canvas.save(tmp_path)
        self.maze_img_ptr, _, _ = self.mlx.mlx_png_file_to_image(self.mlx_init,
                                                                 tmp_path)
        return True

    def draw_pacman(self) -> None:
        """Draw the Pacman sprite on the maze."""
        life = None
        if self.pacman is not None:
            life = self.pacman.lives
        self.pacman: Pacman = self.level_engine.init_maze.pacman
        assert self.pacman is not None
        if life is not None:
            self.pacman.lives = life
        cell_size, margin_x, margin_y = self._grid()

        px: int = int(margin_x + self.pacman.render_x * cell_size)
        py: int = int(margin_y + self.pacman.render_y * cell_size)
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
                                         px + cell_size // 2 - width // 2,
                                         py + cell_size // 2 - height // 2)

    def draw_ghost(self) -> None:
        """Draw the ghost sprite on the maze """

        self.ghosts: list[Ghost] = self.level_engine.init_maze.ghosts
        cell_size, margin_x, margin_y = self._grid()
        color_ghost: dict[str, str] = {
            'R': 'ghost_red',
            'B': 'ghost_blue'
        }

        for ghost in self.ghosts:
            sprite_ghost: str
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

        cell_size, margin_x, margin_y = self._grid()

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

        cell_size, margin_x, margin_y = self._grid()

        for super_pacgum in super_pacgums:
            self._put_sprite_centered(super_pacgum[0],
                                      super_pacgum[1],
                                      img_ptr,
                                      height,
                                      width)
        return True

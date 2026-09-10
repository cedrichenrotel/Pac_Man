from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING
from src.render.utils import (XK_ESCAPE, XK_UP,
                              XK_DOWN, XK_LEFT,
                              XK_RIGHT, get_cell_size,
                              get_asset_path, transform_all_coord_to_cardinal,
                              YELLOW, check_range)
from src.engine.entities import Ghost, Pacman
from src.engine.utils import DIRECTIONS
from mlx import Mlx
from src.engine.model import Config_json
from src.engine.level import Level
from PIL import Image
from time import time
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
                 config: Config_json,
                 highscore: dict[str, int]) -> None:
        self.highscore = highscore
        self.config = config
        self.GameRender = GameRender
        self.width = width
        self.score = 0
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window
        self.pacman: Optional[Pacman] = None

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

    def on_expose(self, param: object) -> None:
        self.render()

    def render(self) -> bool:
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         self.maze_img_ptr, 0, 0)
        self.draw_super_pacgum()
        self.draw_pacgum()
        self.draw_pacman()

        self.draw_ghost()
        self.show_life()
        if self.check_positioning() is False:
            return False
        return True

    def check_positioning(self) -> bool:
        """check the position of all ghost and pacman
        if a ghost grab pacman , pacman decrease
        life and window is refresh.
        also calcul if pacman life is equal to zero is game over
        and return to menu scene
        """

        pacman = self.pacman
        assert pacman is not None

        for ghost in self.ghosts:
            if (check_range(ghost.render_x, pacman.render_x) is True
                and check_range(ghost.render_y,
                                pacman.render_y) is True):
                if ghost.is_edible is False:
                    pacman.decrease_life()
                    self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
                    self.launch()
                else:
                    ghost.eaten = True
                    self.score += self.config.points_per_ghost
                    ghost.init_ghost_eaten()

        if (pacman.lives == 0):
            from src.render.scenes.menu import MenuScene
            self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height, self.config, self.highscore)
            self.GameRender.current_scene.launch()
            return False
        else:
            return True

    def launch(self) -> None:
        '''display the level scene'''

        self.level_engine: Level = Level(self.config)
        self.level_engine.generate_maze(self.config.seed)
        self.maze = self.level_engine.generator.maze
        self.maze_width: int = self.level_engine.config.level.width
        self.maze_height: int = self.level_engine.config.level.height
        if self.draw_maze() is False:
            return
        if self.render() is False:
            return
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)
        self.mlx.mlx_expose_hook(self.mlx_window, self.on_expose, self)
        self.mlx.mlx_loop_hook(self.mlx_init, self.on_loop, self)

    def show_life(self) -> None:
        assert self.pacman is not None
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                10,
                                self.height - 40,
                                YELLOW, f"life: {self.pacman.lives}")

    def on_loop(self, param: object) -> None:
        """ is automatically called by mlx_loop to move forward
            render_x/y moves one step in the x/y direction, drawing the
            intermediate positions """

        self.pacman_moving()
        self.ghost_moving()

    def pacman_moving(self) -> None:
        """handle pacman moving in the maze"""

        assert self.pacman is not None

        if self.pacman.key_direction is not None:
            self.pacman.move(self.pacman.key_direction,
                             self.level_engine.generator)
            self.pacman.frame_index += 1
            if self.pacman.move_render(0.150) is True:
                self.add_point_score(self.pacman)
                self.render()
                self.check_positioning()

    def ghost_moving(self) -> None:
        """handle all ghost moving in the maze"""

        assert self.pacman is not None

        for ghost in self.ghosts:
            ghost.time_is_edible()
            if ghost.path_to_goal:
                if ghost.move(ghost.path_to_goal[0],
                              self.level_engine.generator) is True:
                    ghost.frame_index += 1
                    ghost.path_to_goal.pop(0)
            elif len(ghost.path_to_goal) == 0:
                ghost.path_to_goal = transform_all_coord_to_cardinal(
                    ghost.path_to_pacman(self.level_engine.generator,
                                         self.pacman))
            if ghost.move_render(0.100) is True:
                self.render()
                self.check_positioning()

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
            self.mlx.mlx_loop_hook(self.mlx_init, None, self)
            self.mlx.mlx_expose_hook(self.mlx_window, None, self)
            self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height,
                self.config, self.highscore)
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
        self.level_engine.push_new_score("./highscore", self.highscore)
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
            self.mlx.mlx_loop_hook(self.mlx_init, None, self)
            self.mlx.mlx_expose_hook(self.mlx_window, None, self)
            self.GameRender.current_scene = MenuScene(
                self.GameRender, self.mlx,
                self.mlx_init,
                self.mlx_window,
                self.width, self.height,
                self.config, self.highscore)
            self.GameRender.current_scene.launch()

    def draw_pacman(self) -> None:
        """Draw the Pacman sprite on the maze."""
        life = None
        if self.pacman is not None:
            life = self.pacman.lives

        self.pacman = self.level_engine.init_maze.pacman
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

    def add_point_score(self, pacman: Pacman) -> None:
        """ Add the Super and Pacgum points when Pacman
           eats them and update the Super/Pacgum counts in the maze """

        pacgum_pos: list[tuple[int, int]] = (self.level_engine.
                                             init_maze.pacgum_pos)
        super_pacgum_pos: list[tuple[int, int]] = (self.level_engine.
                                                   init_maze.superpacgum_pos)
        ghosts: list[Ghost] = self.level_engine.init_maze.ghosts

        if pacman.current_pos in pacgum_pos:
            pacgum_pos.remove(pacman.current_pos)
            self.score += self.config.points_per_pacgum
        elif pacman.current_pos in super_pacgum_pos:
            super_pacgum_pos.remove(pacman.current_pos)
            for ghost in ghosts:
                ghost.is_edible = True
                ghost.start_time_is_edible = time()
            self.score += self.config.points_per_super_pacgum

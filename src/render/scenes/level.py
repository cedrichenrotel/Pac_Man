from __future__ import annotations

from collections.abc import Callable
from time import time
from typing import Any
from PIL import ImageDraw
from src.engine.entities import Ghost, Pacman
from src.engine.level import Level
from src.render.draw import Draw
from src.render.utils import (
    LIGHT_GRAY,
    XK_CHEAT_FREEZE,
    XK_CHEAT_GHOSTS_VULN,
    XK_CHEAT_INCREASE_SPEED,
    XK_CHEAT_INVINCIBLE,
    XK_CHEAT_LIFE_ADD,
    XK_CHEAT_SKIP_LEVEL,
    XK_DOWN,
    XK_ESCAPE,
    XK_LEFT,
    XK_RETURN,
    XK_RIGHT,
    XK_UP,
    YELLOW,
    check_range,
    compare_position,
    transform_all_coord_to_cardinal,
    pil_to_mlx_image,
)


class LevelScene(Draw):
    def __init__(self, game: Any) -> None:
        self.game = game
        self.pacman: Pacman | None = None
        self.GameRender = self.game.GameRender
        self.config = self.game.config
        self.mlx = self.game.mlx
        self.mlx_init = self.game.mlx_init
        self.mlx_window = self.game.mlx_window
        self.score = self.game.score
        self.player_name = self.game.player_name
        self.highscore = self.game.highscore
        self.width = self.game.width
        self.score = 0
        self.actual_lvl = 1
        self.height = self.game.height
        self.is_game_over: bool = False
        self.time_eligible: float = 0
        self.pacman_last_position: tuple[float, float] | None = None
        self.is_winning: bool = False
        self.pacgum_pos: list[tuple[int, int]] | None = None
        self.super_pacgum_pos: list[tuple[int, int]] | None = None
        self.cheat_freeze_ghost: bool = False
        self.cheat_invincible: bool = False
        self.last_time: float = time()
        self.move_pac: int = 3
        self.paused: bool = False
        self.hud_img: int | None = None
        self.cheat_img: int | None = None
        self.entries: list[tuple[str, Callable[[], None]]] = [
            ("Return to the main menu", self.quit_game),
            ("Resume the game", self.return_to_game),
        ]
        self.middle_w: int = int(self.width / 2) - 100
        self.middle_h: int = int(self.height / 2) - 100
        self.step: int = 40
        self.selected: int = 0

    def on_expose(self, param: object) -> None:
        if self.paused is True:
            return
        self.render()

    def render(self) -> bool:
        if self.is_winning is True:
            return True
        if self.is_game_over:
            return False
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.mlx.mlx_put_image_to_window(
            self.mlx_init, self.mlx_window, self.maze_img_ptr, 0, 0
        )
        self.mlx.mlx_put_image_to_window(
            self.mlx_init, self.mlx_window, self.pacgum_img_ptr, 0, 0
        )

        self.draw_super_pacgum()
        self.draw_pacman()
        self.draw_ghost()
        self.draw_hud_on_canvas()
        self.draw_cheat()
        if self.check_positioning() is False:
            return False
        return True

    def check_ghost_touch(self, ghost: Ghost, pacman: Pacman) -> None:
        if (
            check_range(ghost.render_x, pacman.render_x, 0.2) is True
            and check_range(ghost.render_y, pacman.render_y, 0.2) is True
        ):
            if ghost.is_edible is False:
                if self.cheat_invincible is False:
                    pacman.decrease_life()
                    pacman.eaten = True
                    for g in self.ghosts:
                        g.eaten = True
                        g.is_edible = False
                        g.init_entities_eaten()
                    pacman.init_entities_eaten()
                    self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
                    self.render()
            else:
                ghost.eaten = True
                ghost.time_respawn = time()
                self.score += self.config.points_per_ghost
                ghost.init_entities_eaten()

    def check_positioning(self) -> bool:
        """check the position of all ghost and pacman
        if a ghost grab pacman , pacman decrease
        life and window is refresh.
        also calcul if pacman life is equal to zero is game over
        and return to menu scene
        """

        if self.is_game_over:
            return False
        if self.is_winning is True:
            return False

        pacman = self.pacman
        assert pacman is not None

        for ghost in self.ghosts:
            self.check_ghost_touch(ghost, pacman)

        if pacman.lives == 0 and pacman.dead is True:
            from src.render.scenes.game_over import GameOver

            self.is_game_over = True
            game_over = GameOver(self)
            game_over.launch()
            return False
        else:
            return True

    def launch(self) -> None:
        """display the level scene"""

        self.level_engine = Level(self.config)
        self.level_engine.generate_maze(self.config.seed)
        self.maze = self.level_engine.generator.maze
        self.process_render()

    def process_render(self) -> None:
        if self.is_winning is True:
            return
        self.maze_width: int = self.level_engine.config.level.width
        self.maze_height: int = self.level_engine.config.level.height
        self.cell_size, self.margin_x, self.margin_y = self._grid()

        if self.draw_maze() is False:
            return
        self.draw_pacgum()
        if self.render() is False:
            return

        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)
        self.mlx.mlx_expose_hook(self.mlx_window, self.on_expose, self)
        self.mlx.mlx_loop_hook(self.mlx_init, self.on_loop, self)
        if self.is_winning is True:
            return

    def on_loop(self, param: object) -> None:
        """is automatically called by mlx_loop to move forward
        render_x/y moves one step in the x/y direction, drawing the
        intermediate positions, executed every tick"""
        if self.paused is True:
            return
        assert self.pacman is not None

        if self.pacman.lives == 0:
            self.render()
            return

        self.pacman_moving()
        if self.is_winning is True:
            return
        self.ghost_moving()

        self.render()
        self.check_positioning()

    def pacman_moving(self) -> None:
        """handle pacman moving in the maze"""
        if self.is_winning is True:
            return
        assert self.pacman is not None

        if self.pacman.key_direction is not None:
            self.pacman.move(
                self.pacman.key_direction, self.level_engine.generator
            )
            if self.pacman.move_render(self.move_pac) is True:
                self.add_point_score(self.pacman)

    def _move_ghost_to_goal(self, ghost: Ghost) -> None:
        """the ghost’s journey to its destination"""

        assert self.pacman is not None
        pos_pac: tuple[float, float] = (
            self.pacman.render_x,
            self.pacman.render_y,
        )
        pos_ghost: tuple[float, float] = (ghost.render_x, ghost.render_y)
        range_val: int = 2
        if (
            ghost.move(ghost.path_to_goal[0], self.level_engine.generator)
            is True
        ):
            ghost.frame_index += 1
            ghost.path_to_goal.pop(0)
        elif (
            compare_position(pos_ghost, pos_pac, range_val) is True
            and self.is_eligible()
        ):
            if (
                self.pacman_last_position is None
                or self.pacman_last_position != pos_pac
            ):
                self.time_eligible = time()
                self.pacman_last_position = pos_pac
                path = ghost.path_to_pacman(
                    self.level_engine.generator,
                    self.pacman,
                    ghost.is_edible,
                )
                ghost.path_to_goal = transform_all_coord_to_cardinal(path)

    def ghost_moving(self) -> None:
        """handle all ghost moving in the maze"""

        if self.is_winning is True:
            return
        assert self.pacman is not None

        if self.cheat_freeze_ghost is False:
            for ghost in self.ghosts:
                if (
                    ghost.time_respawn is not None
                    and time() - ghost.time_respawn <= ghost.respawn_delay
                ):
                    continue
                if ghost.time_respawn is not None:
                    ghost.is_edible = False
                    ghost.time_respawn = None
                    ghost.last_time = time()

                ghost.time_is_edible(self.level_engine.generator, self.pacman)
                if ghost.path_to_goal:
                    self._move_ghost_to_goal(ghost)
                elif len(ghost.path_to_goal) == 0:
                    ghost.path_to_goal = transform_all_coord_to_cardinal(
                        ghost.path_to_pacman(
                            self.level_engine.generator, self.pacman
                        )
                    )
                ghost.move_render(2)

    def is_eligible(self) -> bool:
        actual_time = time()
        if self.time_eligible == 0:
            return True
        if actual_time - self.time_eligible > 2:
            return True
        return False

    def on_key(self, keycode: int, param: object) -> None:
        """go back to the menu scene on escape"""

        pacman: Pacman | None = self.level_engine.init_maze.pacman
        assert pacman is not None
        if keycode == XK_ESCAPE:
            self.go_to_menu()
        if keycode == XK_UP:
            if pacman.key_direction is None:
                pacman.last_time = time()
            pacman.key_direction = "N"
        elif keycode == XK_DOWN:
            if pacman.key_direction is None:
                pacman.last_time = time()
            pacman.key_direction = "S"
        elif keycode == XK_LEFT:
            if pacman.key_direction is None:
                pacman.last_time = time()
            pacman.key_direction = "W"
            if pacman.key_direction is None:
                pacman.last_time = time()
        elif keycode == XK_RIGHT:
            if pacman.key_direction is None:
                pacman.last_time = time()
            pacman.key_direction = "E"
        elif keycode == XK_CHEAT_INVINCIBLE:
            if self.cheat_invincible is False:
                self.cheat_invincible = True
            else:
                self.cheat_invincible = False
        elif keycode == XK_CHEAT_FREEZE:
            if self.cheat_freeze_ghost is False:
                self.cheat_freeze_ghost = True
            else:
                self.cheat_freeze_ghost = False
        elif keycode == XK_CHEAT_SKIP_LEVEL:
            self.winning()
        elif keycode == XK_CHEAT_LIFE_ADD:
            if pacman.lives < self.config.lives:
                pacman.lives += 1
        elif keycode == XK_CHEAT_INCREASE_SPEED:
            if self.move_pac == 3:
                self.move_pac = 5
            else:
                self.move_pac = 3
        elif keycode == XK_CHEAT_GHOSTS_VULN:
            ghosts: list[Ghost] = self.level_engine.init_maze.ghosts
            for ghost in ghosts:
                ghost.is_edible = True
                ghost.start_time_is_edible = time()

    def winning(self) -> None:
        if self.actual_lvl != self.level_engine.lvl_max:
            self.level_engine.next_level()
            self.maze = self.level_engine.generator.maze
            self.process_render()
            self.last_time = time()
            self.actual_lvl += 1
        else:
            from src.render.scenes.win import Winner

            self.is_winning = True
            winner = Winner(self)
            winner.launch()

    def add_point_score(self, pacman: Pacman) -> None:
        """Add the Super and Pacgum points when Pacman
        eats them and update the Super/Pacgum counts in the maze"""

        self.pacgum_pos = self.level_engine.init_maze.pacgum_pos
        self.super_pacgum_pos = self.level_engine.init_maze.superpacgum_pos
        assert self.pacgum_pos is not None
        assert self.super_pacgum_pos is not None
        ghosts: list[Ghost] = self.level_engine.init_maze.ghosts

        if pacman.current_pos in self.pacgum_pos:
            self.revoke_pacgum(pacman.current_pos)
            self.pacgum_pos.remove(pacman.current_pos)
            self.score += self.config.points_per_pacgum
        elif pacman.current_pos in self.super_pacgum_pos:
            self.super_pacgum_pos.remove(pacman.current_pos)
            for ghost in ghosts:
                ghost.is_edible = True
                ghost.start_time_is_edible = time()
            self.score += self.config.points_per_super_pacgum
        if len(self.pacgum_pos) == 0 and len(self.super_pacgum_pos) == 0:
            self.winning()

    def revoke_pacgum(self, pos: tuple[int, int]) -> None:
        """destroy the pacgum at the pos is on the canva of pacgums and
        free the last canva to update the new one whithout the pacgum etead"""

        _, width, height = self.GameRender.sprites_stores.sprites["pacgum"][0]

        px: int = int(self.margin_x + pos[0] * self.cell_size)
        py: int = int(self.margin_y + pos[1] * self.cell_size)
        rect_x = px + self.cell_size // 2 - width // 2
        rect_y = py + self.cell_size // 2 - height // 2

        draw = ImageDraw.Draw(self.canvas_pacgum)
        draw.rectangle(
            [rect_x, rect_y, rect_x + width, rect_y + height],
            fill=(0, 0, 0, 0),
        )

        if hasattr(self.mlx, "mlx_destroy_image"):
            self.mlx.mlx_destroy_image(self.mlx_init, self.pacgum_img_ptr)
        self.pacgum_img_ptr = pil_to_mlx_image(
            self.canvas_pacgum, "pacgum_cache.png", self.mlx_init, self.mlx
        )

    def quit_game(self) -> None:
        self.mlx.mlx_loop_hook(self.mlx_init, None, self)
        self.mlx.mlx_expose_hook(self.mlx_window, None, self)

        if len(self.player_name) != 0:
            from src.render.scenes.menu import MenuScene

            self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
            self.GameRender.current_scene = MenuScene(self)
            self.GameRender.current_scene.launch()
        else:
            from src.render.scenes.player import PlayerScene

            player = PlayerScene(self)
            player.launch()

    def go_to_menu(self) -> None:
        """open the pause menu and hand key control to on_key_break"""

        self.time_when_pause = time()
        self.paused = True
        self.selected = 0
        self.draw_menu()
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key_break, self)

    def return_to_game(self) -> None:
        """close the pause menu and give control back to on_key"""

        time_during_break = time() - self.time_when_pause
        self.last_time = self.last_time + time_during_break

        self.paused = False
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)
        self.render()

    def draw_selector(self, x: int, y: int) -> None:
        """draw the selector '>' of menu"""

        height = 12
        for dy in range(-height // 2, height // 2 + 1):
            width = height // 2 - abs(dy)
            for dx in range(width):
                self.mlx.mlx_pixel_put(
                    self.mlx_init, self.mlx_window, x + dx, y + dy, LIGHT_GRAY
                )

    def draw_menu(self) -> None:
        """install the title with them redirections"""
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        for i, (label, _action) in enumerate(self.entries):
            y = self.middle_h + self.step * i
            if i == self.selected:
                self.draw_selector(self.middle_w - 20, y + 10)
            self.mlx.mlx_string_put(
                self.mlx_init, self.mlx_window, self.middle_w, y, YELLOW, label
            )

    def on_key_break(self, keycode: int, param: object) -> None:
        """record the key press and do the action
        key up to go up, key down to go down,
        enter to select the title"""

        if keycode == XK_UP:
            self.selected = (self.selected - 1) % len(self.entries)
            self.draw_menu()
        elif keycode == XK_DOWN:
            self.selected = (self.selected + 1) % len(self.entries)
            self.draw_menu()
        elif keycode == XK_RETURN:
            self.entries[self.selected][1]()

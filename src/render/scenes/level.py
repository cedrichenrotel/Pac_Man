from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from src.render.utils import (XK_ESCAPE, XK_UP,
                              XK_DOWN, XK_LEFT,
                              XK_RIGHT,
                              transform_all_coord_to_cardinal,
                              check_range)
from src.render.draw import Draw
from src.engine.entities import Ghost, Pacman
from src.engine.model import Config_json
from src.engine.level import Level
from mlx import Mlx
from time import time
# guarded to avoid a circular import: GameRender.py imports LevelScene at
# module level, so GameRender can only be imported here for type hints
if TYPE_CHECKING:
    from src.render.game import GameRender


class LevelScene(Draw):

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
        self.player_name = player_name
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
        self.game_over: bool = False

    def on_expose(self, param: object) -> None:
        self.render()

    def render(self) -> bool:
        if self.game_over:
            return False
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.mlx.mlx_put_image_to_window(self.mlx_init,
                                         self.mlx_window,
                                         self.maze_img_ptr, 0, 0)
        self.draw_super_pacgum()
        self.draw_pacgum()
        self.draw_pacman()
        self.draw_ghost()
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

        if self.game_over:
            return False

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

        if pacman.lives == 0 and pacman.dead is True:
            self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
            if len(self.player_name) != 0:
                if len(self.level_engine.player_name) == 0:
                    self.level_engine.highscore = self.highscore
                    self.level_engine.add_player_name(self.player_name)
                    self.level_engine.add_score(self.score)
                    self.level_engine.push_new_score("./highscore",
                                                     self.highscore)
                self.go_to_menu()
                return False
            else:
                from src.render.scenes.player import PlayerScene
                player = PlayerScene(
                    self.GameRender, self.mlx,
                    self.mlx_init,
                    self.mlx_window,
                    self.width, self.height, self.config, self.highscore,
                    self.player_name, self.score)
                player.launch()
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
        self.cell_size, self.margin_x, self.margin_y = self._grid()
        if self.draw_maze() is False:
            return
        if self.render() is False:
            return
        self.show_life()
        self.show_score()
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)
        self.mlx.mlx_expose_hook(self.mlx_window, self.on_expose, self)
        self.mlx.mlx_loop_hook(self.mlx_init, self.on_loop, self)

    def on_loop(self, param: object) -> None:
        """ is automatically called by mlx_loop to move forward
            render_x/y moves one step in the x/y direction, drawing the
            intermediate positions, executed every tick """

        assert self.pacman is not None

        if self.pacman.lives == 0:
            self.render()
            return

        self.pacman_moving()
        self.ghost_moving()

        self.render()
        self.check_positioning()

    def pacman_moving(self) -> None:
        """handle pacman moving in the maze"""

        assert self.pacman is not None

        if self.pacman.key_direction is not None:
            self.pacman.move(self.pacman.key_direction,
                             self.level_engine.generator)
            self.pacman.frame_index += 1
            if self.pacman.move_render(0.150) is True:
                self.add_point_score(self.pacman)

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
            ghost.move_render(0.100)

    def on_key(self, keycode: int, param: object) -> None:
        '''go back to the menu scene on escape'''

        pacman: Pacman | None = self.level_engine.init_maze.pacman
        assert pacman is not None

        if keycode == XK_ESCAPE:
            self.go_to_menu()
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
            if len(self.level_engine.player_name) == 0:
                self.level_engine.add_player_name(self.player_name)
            if self.score > self.level_engine.score:
                self.level_engine.add_score(self.score)
            self.level_engine.next_level()
            self.maze = self.level_engine.generator.maze
            self.render()
        else:
            # si jamais le nombre de level max etait atteind, on reviens
            # au menu. egalement on devrait plus tard ajouter le score
            # au highscore
            if self.score > self.level_engine.score:
                self.level_engine.add_score(self.score)
            from src.render.scenes.player import PlayerScene
            if len(self.player_name) != 0:
                self.go_to_menu()
            else:
                player = PlayerScene(
                    self.GameRender, self.mlx,
                    self.mlx_init,
                    self.mlx_window,
                    self.width, self.height, self.config, self.highscore,
                    self.player_name, self.score)
                player.launch()

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

    def go_to_menu(self) -> None:
        """ exits the current level and returns to the menu screen
            clears the window and deactivates the hooks before
            the transition """

        self.mlx.mlx_loop_hook(self.mlx_init, None, self)
        self.mlx.mlx_expose_hook(self.mlx_window, None, self)

        from src.render.scenes.menu import MenuScene
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.GameRender.current_scene = MenuScene(
            self.GameRender, self.mlx,
            self.mlx_init,
            self.mlx_window,
            self.width, self.height, self.config, self.highscore,
            self.player_name, self.score)
        self.GameRender.current_scene.launch()

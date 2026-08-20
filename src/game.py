from src.scenes.menu import MenuScene
from mlx import Mlx
# import time


class Game():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.running = True
        self.mlx = Mlx()

    def run(self):
        self.mlx_init = self.mlx.mlx_init()
        if self.mlx_init is None:
            return
        self.mlx_window = self.mlx.mlx_new_window(self.mlx_init, self.width,
                                                  self.height, "Pac-Man")
        if self.mlx_window is None:
            return
        self.current_scene = MenuScene(self, self.mlx, self.mlx_init,
                                       self.mlx_window,
                                       self.width,
                                       self.height)
        self.current_scene.launch()
        self.mlx.mlx_loop(self.mlx_init)
        self.mlx.mlx_release(self.mlx_init)

    def change_scene(self, new_scene):
        self.current_scene = new_scene

    def start_game(self):
        print("start game (TODO: scene level)")

    def show_highscores(self):
        print("show highscores (TODO: scene score)")

    def show_instructions(self):
        print("show instructions (TODO)")

    def quit_game(self):
        self.running = False
        self.mlx.mlx_loop_exit(self.mlx_init)

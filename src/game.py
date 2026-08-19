from src.scenes.menu import MenuScene
from mlx import Mlx
import time


class Game():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.running = True
        self.mlx = Mlx()

    def change_scene(self, new_scene):
        self.current_scene = new_scene

    def run(self):
        mlx_init = self.mlx.mlx_init()
        if (mlx_init is None):
            # soit terminer le code soit relancer ?
            pass
        mlx_window = self.mlx.mlx_new_window(mlx_init, self.width,
                                             self.height, "Pac-Man")
        if (mlx_window is None):
            # soit terminer le code soit relancer ?
            pass
        self.current_scene = MenuScene(self.mlx, mlx_init, mlx_window,
                                       self.width, self.height)
        # self.mlx.mlx_loop(mlx_init)
        self.current_scene.launch()
        # self.mlx.mlx_loop(mlx_init)
        print("test")
        time.sleep(2)
        # a changer par la boucle
        # while self.running:
        #     pass
        self.mlx.mlx_release(mlx_init)

    # def change_scene(self):
    #     pass

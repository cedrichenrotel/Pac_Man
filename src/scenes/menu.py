from src.scenes.base import Scene
from src.utils import make_color

red = make_color(255, 0, 0, 0)
green = make_color(0, 255, 0, 0)
blue = make_color(0, 0, 255, 0)
black = make_color(0, 0, 0, 255)
LIGHT_GRAY = make_color(200, 200, 200)
GRAY = make_color(128, 128, 128)
DARK_GRAY = make_color(60, 60, 60)


class MenuScene(Scene):
    def __init__(self, mlx, mlx_init, mlx_window, width, height):
        self.width = width
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window

    def get_calc(self):
        self.middle_w = int(self.width / 2) - 100
        self.middle_h = int(self.height / 2) - 100
        self.step = 40

    def write_banner(self, width, height):
        for i in range(1, 150):
            self.mlx.mlx_pixel_put(self.mlx_init, self.mlx_window, width + i,
                                   height, GRAY)
            self.mlx.mlx_pixel_put(self.mlx_init, self.mlx_window, width + i,
                                   height + 20, GRAY)

    def write_title(self):
        self.write_banner(self.middle_w, self.middle_h)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window, self.middle_w,
                                self.middle_h, 255, "Start Game")

        self.write_banner(self.middle_w, self.middle_h + self.step)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window, self.middle_w,
                                self.middle_h + self.step,
                                255, "View Highscores")

        self.write_banner(self.middle_w, self.middle_h + self.step*2)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window, self.middle_w,
                                self.middle_h + self.step*2,
                                255, "Instructions")

        self.write_banner(self.middle_w, self.middle_h + self.step*3)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window, self.middle_w,
                                self.middle_h + self.step*3, red,
                                "Exit")

    def launch(self):
        self.get_calc()
        self.write_title()
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)


# def mymouse(button, x, y, mystuff):
#     print(f"Got mouse event! button {button} at {x},{y}.")


# def mykey(keynum, mystuff):
#     print(f"Got key {keynum}, and got my stuff back:")
#     print(mystuff)
#     if keynum == 32:
#         m.mlx_mouse_hook(win_ptr, None, None)

# from mlx import Mlx
# m = Mlx()
# mlx_ptr = m.mlx_init()
# win_ptr = m.mlx_new_window(mlx_ptr, 200, 200, "toto")
# m.mlx_clear_window(mlx_ptr, win_ptr)
# m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
# # (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
# # print(f"Got screen size: {w} x {h} .")

# # stuff = [1, 2]
# # m.mlx_mouse_hook(win_ptr, mymouse, None)
# # m.mlx_key_hook(win_ptr, mykey, stuff)

# m.mlx_loop(mlx_ptr)

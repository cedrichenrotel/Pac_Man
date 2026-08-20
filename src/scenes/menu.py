from src.scenes.base import Scene
from src.utils import make_color
from PIL import Image
import os

red = make_color(255, 0, 0, 0)
green = make_color(0, 255, 0, 0)
blue = make_color(0, 0, 255, 0)
black = make_color(0, 0, 0, 255)
LIGHT_GRAY = make_color(200, 200, 200)
GRAY = make_color(128, 128, 128)
DARK_GRAY = make_color(60, 60, 60)
YELLOW = make_color(255, 255, 0)


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

    # def write_banner(self, width, height):
    #     for i in range(1, self.step):
    #         self.mlx.mlx_pixel_put(self.mlx_init, self.mlx_window,
    #                                width, height + i, GRAY)
    #     for i in range(1, 150):
    #         self.mlx.mlx_pixel_put(self.mlx_init, self.mlx_window, width + i,
    #                                height, GRAY)
    #         self.mlx.mlx_pixel_put(self.mlx_init, self.mlx_window, width + i,
    #                                height + 20, GRAY)

    def write_title(self):
        # self.write_banner(self.middle_w, self.middle_h)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window, self.middle_w,
                                self.middle_h, YELLOW, "Start Game")

        # self.write_banner(self.middle_w, self.middle_h + self.step)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window, self.middle_w,
                                self.middle_h + self.step,
                                YELLOW, "View Highscores")

        # self.write_banner(self.middle_w, self.middle_h + self.step*2)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window, self.middle_w,
                                self.middle_h + self.step*2,
                                YELLOW, "Instructions")

        # self.write_banner(self.middle_w, self.middle_h + self.step*3)
        self.mlx.mlx_string_put(self.mlx_init, self.mlx_window, self.middle_w,
                                self.middle_h + self.step*3, YELLOW,
                                "Exit")

    def install_menu_image(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "./../../assets/menu/menu_logo.png")
        image_path = os.path.normpath(image_path)
        Image.open(image_path).convert("RGBA").save(image_path)

        self.img = self.mlx.mlx_png_file_to_image(self.mlx_init, image_path)
        img_ptr, img_width, img_height = self.img

        left_space = self.width - img_width

        if img_ptr:
            self.mlx.mlx_put_image_to_window(self.mlx_init, self.mlx_window,
                                             img_ptr, int(left_space / 2), 0)

    def launch(self):
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.get_calc()
        self.install_menu_image()
        self.write_title()
        self.mlx.mlx_do_sync(self.mlx_init)

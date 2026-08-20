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

XK_UP = 65362
XK_DOWN = 65364
XK_RETURN = 65293


class MenuScene(Scene):
    def __init__(self, game, mlx, mlx_init, mlx_window, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.mlx_window = mlx_window
        self.selected = 0
        self.entries = [
              ("Start Game", self.game.start_game),
              ("View Highscores", self.game.show_highscores),
              ("Instructions", self.game.show_instructions),
              ("Exit", self.game.quit_game),
          ]

    def get_calc(self):
        self.middle_w = int(self.width / 2) - 100
        self.middle_h = int(self.height / 2) - 100
        self.step = 40

    def draw_selector(self, x, y):
        height = 12
        for dy in range(-height // 2, height // 2 + 1):
            width = height // 2 - abs(dy)
            for dx in range(width):
                self.mlx.mlx_pixel_put(self.mlx_init, self.mlx_window,
                                       x + dx, y + dy, LIGHT_GRAY)

    def draw_menu(self):
        self.mlx.mlx_clear_window(self.mlx_init, self.mlx_window)
        self.install_menu_image()
        for i, (label, _action) in enumerate(self.entries):
            y = self.middle_h + self.step * i
            if i == self.selected:
                self.draw_selector(self.middle_w - 20, y + 10)
            self.mlx.mlx_string_put(self.mlx_init, self.mlx_window,
                                    self.middle_w, y, YELLOW, label)

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

    def on_key(self, keycode, param):
        if keycode == XK_UP:
            self.selected = (self.selected - 1) % len(self.entries)
            self.draw_menu()
        elif keycode == XK_DOWN:
            self.selected = (self.selected + 1) % len(self.entries)
            self.draw_menu()
        elif keycode == XK_RETURN:
            self.entries[self.selected][1]()

    def launch(self):
        self.get_calc()
        self.draw_menu()
        self.mlx.mlx_key_hook(self.mlx_window, self.on_key, self)

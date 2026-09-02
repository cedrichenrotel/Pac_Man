import sys

try:
    from typing import Optional, Any, TYPE_CHECKING
    from mlx import Mlx
    from src.colors import COLORS
    from src.render.utils import get_asset_path
    import os
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit(1)

if TYPE_CHECKING:
    from src.render.game import GameRender


class SpriteStores():

    def __init__(self, GameRender: 'GameRender', mlx: Mlx,
                 mlx_init: Optional[int]) -> None:

        self.GameRender = GameRender
        self.mlx = mlx
        self.mlx_init = mlx_init
        self.sprites: dict[str, list[Any]] = {}

    def load(self, name: str, path: str) -> None:
        """ provides the path so that Python can retrieve the images """

        image_path: str = get_asset_path(path)

        if name not in self.sprites:
            self.sprites[name]: list[Any] = []
        img = self.mlx.mlx_png_file_to_image(self.mlx_init, image_path)
        if img[0] is None:
            raise ValueError("def load(): Failed to load image")
        self.sprites[name].append(img)

    def load_folder(self, name: str, folder: str) -> None:
        """ list and sort the files in a folder before calling load() """

        folder_path: str = get_asset_path(folder)
        list_file: list[str] = sorted(os.listdir(folder_path))

        for file in list_file:
            full_path: str = os.path.join(folder, file)
            self.load(name, full_path)

    def load_all(self) -> None:
        """ The program stores the images in memory """

        self.load('wall', "sprites/wall/wall.png")
        self.load('pacgum', "sprites/pacgum/pacgum.png")
        self.load('super_pacgum', "sprites/pacgum/super_pacgum.png")
        self.load_folder('ghost_red', "sprites/ghost/ghost_red")
        self.load_folder('ghost_blue', "sprites/ghost/ghost_blue")
        self.load_folder('pacman', "sprites/pacman")

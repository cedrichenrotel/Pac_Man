from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, Any

from PIL import Image

if TYPE_CHECKING:
    from mlx import Mlx


HUD_TOP_HEIGHT: int = 80
HUD_BOTTOM_HEIGHT: int = 50


def make_color(r: int, g: int, b: int, a: int = 255) -> int:
    """Install RGBA components into a single integer color."""

    return r | (g << 8) | (b << 16) | (a << 24)


RED: int = make_color(255, 0, 0)
CREAM: int = make_color(233, 218, 223)
LIGHT_GRAY: int = make_color(200, 200, 200)
YELLOW: int = make_color(255, 255, 0)

XK_UP: int = 65362
XK_DOWN: int = 65364
XK_RETURN: int = 65293
XK_ESCAPE: int = 65307
XK_LEFT: int = 65361
XK_RIGHT: int = 65363
XK_BACK: int = 65288
XK_CHEAT_INVINCIBLE: int = 49
XK_CHEAT_FREEZE: int = 50
XK_CHEAT_SKIP_LEVEL: int = 51
XK_CHEAT_LIFE_ADD: int = 52
XK_CHEAT_INCREASE_SPEED: int = 53
XK_CHEAT_GHOSTS_VULN: int = 54

list_key = [
    (113, "Q"),
    (119, "W"),
    (101, "E"),
    (114, "R"),
    (116, "T"),
    (121, "Y"),
    (117, "U"),
    (105, "I"),
    (111, "O"),
    (112, "P"),
    (97, "A"),
    (115, "S"),
    (100, "D"),
    (102, "F"),
    (103, "G"),
    (104, "H"),
    (106, "J"),
    (107, "K"),
    (108, "L"),
    (122, "Z"),
    (120, "X"),
    (99, "C"),
    (118, "V"),
    (98, "B"),
    (110, "N"),
    (109, "M"),
    (49, "1"),
    (50, "2"),
    (51, "3"),
    (52, "4"),
    (53, "5"),
    (54, "6"),
    (55, "7"),
    (56, "8"),
    (57, "9"),
    (48, "0"),
]


def transform_all_coord_to_cardinal(
    coords: list[tuple[int, int]],
) -> list[str]:
    """transform list of coord tuple to list of coordinate cardinal (NSEW)"""
    cardinal_list: list[str] = []
    for i in range(len(coords) - 1):
        cardinal_list.append(get_cardinal_directions(coords[i], coords[i + 1]))
    return cardinal_list


def get_cardinal_directions(
    from_coord: tuple[int, int], to: tuple[int, int]
) -> str:
    """get cardinal coordinate from coord (x, y) to (x, y)"""
    if from_coord[0] > to[0] and from_coord[1] == to[1]:
        return "W"
    elif from_coord[0] < to[0] and from_coord[1] == to[1]:
        return "E"
    elif from_coord[1] > to[1] and from_coord[0] == to[0]:
        return "N"
    else:
        return "S"


def clear_rect(
    mlx: Mlx,
    mlx_ptr: int,
    win_ptr: int,
    x: int,
    y: int,
    width: int,
    height: int,
    color: int = CREAM,
) -> None:
    """erase a rectangular area of the window by overpainting it, so only
    part of the display needs to be redrawn instead of the whole window"""

    for dy in range(height):
        for dx in range(width):
            mlx.mlx_pixel_put(mlx_ptr, win_ptr, x + dx, y + dy, color)


def get_asset_path(path: str) -> str:
    """convert a relative path to 'assets/’ into a usable absolute path,
    regardless of where the programme is launched from"""
    base_dir: str
    if getattr(sys, "frozen", False):
        base_dir = os.path.join(sys._MEIPASS, "assets")  # type: ignore
    else:
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(current_dir, "../../assets/")
    return os.path.join(base_dir, path)


def get_cell_size(
    width: int,
    height: int,
    maze_width: int,
    maze_height: int,
    margin: int = 0,
    tile: int = 1,
) -> int:
    """calculate the number of pixels in a cell, reserving `margin`
    pixels on each side so bordering walls can be centered without
    being clipped by the window edge, and rounded down to a multiple
    of `tile` (the wall sprite size) so wall tiling never overshoots
    a cell and misaligns at junctions"""

    cell_size_x: int = (width - margin * 2) // maze_width
    cell_size_y: int = (height - margin * 2) // maze_height
    cell_size: int = min(cell_size_x, cell_size_y)
    if tile > 1:
        cell_size = (cell_size // tile) * tile
    return cell_size


def check_range(from_val: float, to_val: float, range_val: float) -> bool:
    """calcul the distance between from_val and to_val ,
    if distance is less than 0.1 return True,
    otherwise return false"""

    from_val = round(from_val, 2)
    to_val = round(to_val, 2)
    distance = abs(from_val - to_val)

    if distance <= range_val:
        return True

    return False


def compare_position(
    pos_ghost: tuple[float, float],
    pos_pac: tuple[float, float],
    range_val: float,
) -> bool:
    """Returns true if the positions of Pac-Man and the ghost are within
    (range_val) of each other along the x and y axes"""

    x_ghost, y_ghost = pos_ghost
    x_pac, y_pac = pos_pac
    if check_range(x_ghost, x_pac, range_val) and check_range(
        y_ghost, y_pac, range_val
    ):
        return True
    return False


def install_menu_image(
    path: str,
    mlx: Mlx,
    mlx_init: int,
    mlx_window: int,
    width: int,
    height: int,
    center: bool = True,
) -> tuple[int | None, int, int]:
    """install in the scene an image from assets/"""

    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    image_path = os.path.join(project_root, path)
    image_path = os.path.normpath(image_path)
    Image.open(image_path).convert("RGBA").save(image_path)

    img: tuple[int | None, int, int] = mlx.mlx_png_file_to_image(
        mlx_init, image_path
    )
    img_ptr, img_width, img_height = img

    x = width - img_width
    y = height - img_height
    if img_ptr:
        if center is not True:
            mlx.mlx_put_image_to_window(
                mlx_init, mlx_window, img_ptr, int(x / 2), 0
            )
        else:
            mlx.mlx_put_image_to_window(
                mlx_init, mlx_window, img_ptr, int(x / 2), int(y / 2)
            )

    return img


def pil_to_mlx_image(
    canvas: Image.Image, filename: str, mlx_init: int | None, mlx: Mlx
) -> Any:
    """saves the image to a .cache folder if it does not exist, stores it
    on the hard drive and displays the image"""
    os.makedirs(".cache", exist_ok=True)
    path = os.path.join(".cache", filename)
    canvas.save(path)
    ptr, _, _ = mlx.mlx_png_file_to_image(mlx_init, path)
    return ptr

import os


def make_color(r: int, g: int, b: int, a: int = 255,
               text: bool = False) -> int:
    '''Install RGBA components into a single integer color.'''

    if text is True:
        return b | (g << 8) | (r << 16) | (a << 24)
    return r | (g << 8) | (b << 16) | (a << 24)


'''basics color for mlx'''
red: int = make_color(255, 0, 0, )
green: int = make_color(0, 255, 0)
BLUE: int = make_color(0, 0, 255)
black: int = make_color(0, 0, 0)
LIGHT_GRAY: int = make_color(200, 200, 200)
GRAY: int = make_color(128, 128, 128)
DARK_GRAY: int = make_color(60, 60, 60)
YELLOW: int = make_color(255, 255, 0)

RED_PIX: int = make_color(255, 0, 0, text=True)
GREEN_PIX: int = make_color(0, 255, 0, text=True)
BLUE_PIX: int = make_color(0, 0, 255, text=True)
BLACK_PIX: int = make_color(0, 0, 0, text=True)
LIGHT_GRAY_PIX: int = make_color(200, 200, 200, text=True)
GRAY_PIX: int = make_color(128, 128, 128, text=True)
DARK_GRAY_PIX: int = make_color(60, 60, 60, text=True)
YELLOW_PIX: int = make_color(255, 255, 0, text=True)

'''key value to record them event'''
XK_UP: int = 65362
XK_DOWN: int = 65364
XK_RETURN: int = 65293
XK_ESCAPE: int = 65307
XK_LEFT: int = 65361
XK_RIGHT = 65363


def transform_all_coord_to_cardinal(coords: list[tuple[int,
                                                       int]]) -> list[str]:
    cardinal_list: list[str] = []
    for i in range(0, len(coords)-1):
        cardinal_list.append(get_cardinal_directions(coords[i], coords[i+1]))
    return cardinal_list


def get_cardinal_directions(from_coord: tuple[int, int],
                            to: tuple[int, int]) -> str:
    """get cardinal coordinate from coord (x, y) to (x, y) """
    if from_coord[0] > to[0] and from_coord[1] == to[1]:
        return 'W'
    elif from_coord[0] < to[0] and from_coord[1] == to[1]:
        return 'E'
    elif from_coord[1] > to[1] and from_coord[0] == to[0]:
        return 'N'
    else:
        return 'S'


def get_asset_path(path: str) -> str:
    """ convert a relative path to 'assets/’ into a usable absolute path,
        regardless of where the programme is launched from """

    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../../assets/", path)


def get_cell_size(width: int, height: int, maze_width: int,
                  maze_height: int, margin: int = 0, tile: int = 1) -> int:
    """ calculate the number of pixels in a cell, reserving `margin`
        pixels on each side so bordering walls can be centered without
        being clipped by the window edge, and rounded down to a multiple
        of `tile` (the wall sprite size) so wall tiling never overshoots
        a cell and misaligns at junctions """

    cell_size_x: int = (width - margin * 2) // maze_width
    cell_size_y: int = (height - margin * 2) // maze_height
    cell_size: int = min(cell_size_x, cell_size_y)
    if tile > 1:
        cell_size = (cell_size // tile) * tile
    return cell_size


def check_range(from_val: float, to_val: float) -> bool:
    """calcul the distance between from_val and to_val ,
    if distance is less than 0.1 return True,
    otherwise return false """

    from_val = round(from_val, 2)
    to_val = round(to_val, 2)
    distance = abs(from_val - to_val)

    if distance <= 0.1:
        return True

    return False

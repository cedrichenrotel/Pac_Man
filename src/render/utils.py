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

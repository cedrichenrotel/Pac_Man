def make_color(r: int, g: int, b: int, a: int = 255) -> int:
    '''Install RGBA components into a single integer color.'''
    return r | (g << 8) | (b << 16) | (a << 24)


'''basics color'''
red: int = make_color(255, 0, 0, 0)
green: int = make_color(0, 255, 0, 0)
blue: int = make_color(0, 0, 255, 0)
black: int = make_color(0, 0, 0, 255)
LIGHT_GRAY: int = make_color(200, 200, 200)
GRAY: int = make_color(128, 128, 128)
DARK_GRAY: int = make_color(60, 60, 60)
YELLOW: int = make_color(255, 255, 0)

'''key value to record them event'''
XK_UP: int = 65362
XK_DOWN: int = 65364
XK_RETURN: int = 65293
XK_ESCAPE: int = 65307

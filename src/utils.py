
def make_color(r: int, g: int, b: int, a: int = 255) -> int:
    return r | (g << 8) | (b << 16) | (a << 24)

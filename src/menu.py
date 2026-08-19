import ctypes
from mlx import Mlx

# libmlx.so utilise strlcpy (fonction BSD) sans lier libbsd correctement,
# on la precharge en RTLD_GLOBAL pour que le symbole soit resolu au chargement.
ctypes.CDLL("libbsd.so.0", mode=ctypes.RTLD_GLOBAL)


def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")


def mykey(keynum, mystuff):
    print(f"Got key {keynum}, and got my stuff back:")
    print(mystuff)
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)


m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 200, 200, "toto")
m.mlx_clear_window(mlx_ptr, win_ptr)
m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
(ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
print(f"Got screen size: {w} x {h} .")

stuff = [1, 2]
m.mlx_mouse_hook(win_ptr, mymouse, None)
m.mlx_key_hook(win_ptr, mykey, stuff)

m.mlx_loop(mlx_ptr)
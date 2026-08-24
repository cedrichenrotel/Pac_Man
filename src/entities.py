import sys
try:
    from mazegenerator import MazeGenerator
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()


class Entities():

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def move(self, direction: str, maze: MazeGenerator) -> bool:
        """ allows entities to move through the maze without
            passing through walls """

        directions: dict[str, tuple] = {
            'N': (0, -1, 1),
            'E': (1, 0, 2),
            'S': (0, 1, 4),
            'W': (-1, 0, 8)
        }
        dx, dy, code = directions[direction]  # deballe le tuple existant dx = 0, dy = -1, code = 1

        if maze.maze[self.y][self.x] & code == 0:  # verifie si il n'y pas de mur sur pos dx,dy
            self.x += dx
            self.y += dy
            return True
        return False


class Pacman(Entities):

    def __init__(self, x: int, y: int, lives: int) -> None:
        super().__init__(x, y)
        self.lives: int = lives


class Ghost(Entities):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.eaten: bool = False  # mangé
        self.is_edible: bool = False  # est comestible

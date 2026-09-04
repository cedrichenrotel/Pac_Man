import sys
from src.colors import COLORS
try:
    import json
    import os
    from pathlib import Path
    from mazegenerator import MazeGenerator
    from src.engine.parse_config import parse_highscore
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()


DIRECTIONS: dict[str, tuple[int, int, int]] = {
            'N': (0, -1, 1),
            'E': (1, 0, 2),
            'S': (0, 1, 4),
            'W': (-1, 0, 8)
        }


def clean_lines_comments(line: str, copie_upto: int) -> tuple[list[str], bool]:
    """ Returns the elements of the line that are not part of a comment and
        a boolean value indicating whether the line is within an
        unclosed comment block """

    in_block_comment: bool = False
    in_string: bool = False
    backslash_count: int = 0
    rst: list[str] = []

    for j, c in enumerate(line):
        if j < copie_upto:
            continue
        if c == '"' and backslash_count % 2 == 0:
            in_string = not in_string
        if c == '\\':
            backslash_count += 1
        else:
            backslash_count = 0

        if (c == '#' or line[j:j+2] == '//') and not in_string:
            rst.append(line[copie_upto:j])
            break
        if line[j:j+2] == '/*' and not in_string:

            for n in range(j+2, len(line)):
                if line[n:n+2] == '*/':
                    rst.append(line[copie_upto:j])
                    copie_upto = n + 2
                    break
            else:
                rst.append(line[copie_upto:j])
                in_block_comment = True
                break
    else:
        rst.append(line[copie_upto:])
    return rst, in_block_comment


def check_comments(data: str) -> str:
    """ extracts uncommented elements (those without #, // or /* */) and
        tidies up the lines """

    rst: list[str] = []
    in_block_comment: bool = False
    data_lines: list[str] = data.split('\n')

    for i, line in enumerate(data_lines):

        if in_block_comment is True:
            pos = line.find('*/')
            if pos != -1:
                copie_upto: int = pos + 2
                in_block_comment = False
            else:
                data_lines[i] = ''
                continue

        else:
            copie_upto = 0

        rst, in_block_comment = clean_lines_comments(line, copie_upto)

        data_lines[i] = ''.join(rst)
    data_clean: str = '\n'.join(data_lines)
    return data_clean


def get_corners(maze: MazeGenerator) -> dict[str, tuple[int, int]]:
    """ locating the four corners of the maze dans un dict """

    height: int = len(maze.maze) - 1
    width: int = len(maze.maze[0]) - 1

    return {
     'top_left': (0, 0),
     'top_right': (width, 0),
     'low_left': (0, height),
     'low_right': (width, height)
    }


def get_center_maze(maze: MazeGenerator) -> tuple[int, int]:
    """ locates the centre of the maze """

    height: int = len(maze.maze)
    width: int = len(maze.maze[0])
    center_pos: tuple[int, int] = (width // 2, height // 2)
    best_pos: tuple[int, int] = center_pos
    best_dist: float = float('inf')  # distance inconnu

    for y, line in enumerate(maze.maze):
        for x, val in enumerate(line):
            if val != 15:
                distance: int = abs(x - center_pos[0]) + abs(y - center_pos[1])
                if best_dist > distance:
                    best_dist = distance
                    best_pos = (x, y)
    return (best_pos)


def create_json_missing(file: Path) -> bool:
    if file.exists() is False:
        file.touch()
        return False
    return True


def push_json(highscore: dict[str, int], path: str) -> None:
    try:
        with open(path, "w", encoding="utf-8"):
            pass
        with open(path, "w", encoding="utf-8") as f:
            json.dump(highscore, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
              f"cannot push new scores in highscores: {e}")


def order_asc_and_limit(highscore: dict[str, int]) -> None:
    sorted_items = sorted(highscore.items(),
                          key=lambda item: item[1],
                          reverse=True)[:10]
    highscore.clear()
    highscore.update(sorted_items)
    push_json(highscore, "./highscore.json")


def install_score_system(path: str, file: Path) -> dict[str, int]:
    """ create highscore.json if missing otherwise
    parse the json """

    highscores: dict[str, int] = {}
    if create_json_missing(file) is True:
        is_highscore_good_format: bool = parse_highscore(file, path)
        if is_highscore_good_format is False:
            os.remove(path)
            create_json_missing(file)
        elif os.stat(file).st_size != 0:
            with open(path) as f:
                highscores = json.load(f)
            order_asc_and_limit(highscores)
    return highscores


def algo_fixed_walk(render: float, x: int) -> float:
    """ Fixed-point method for fluid displacement """

    vitesse: float = 0.1
    if render < x:
        render = min(render + vitesse, x)
    elif render > x:
        render = max(render - vitesse, x)
    return render

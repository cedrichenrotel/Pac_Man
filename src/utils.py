import sys
try:
    from mazegenerator import MazeGenerator
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()


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

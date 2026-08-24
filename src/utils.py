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
            copie_upto: int = 0

        rst, in_block_comment = clean_lines_comments(line, copie_upto)

        data_lines[i] = ''.join(rst)
    data_clean: str = '\n'.join(data_lines)
    return data_clean


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

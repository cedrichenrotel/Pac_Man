def clean_lines_comments(line: str, copie_upto: int) -> tuple[list[str], bool]:
    """ returns the elements in the line that are not part of a comment """

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
    """ supports comments. Lines beginning with “#” are comments
        and should be ignored """

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

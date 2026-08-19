""" supports comments. Lines beginning with “#” are comments """
"""and should be ignored """
def check_comments(data: str) -> str:

    data_lines: list[str] = data.split('\n')
    list_comment: list[str] = [
        '/*',
        '*/',
        '//'
    ]

    for i, line in enumerate(data_lines):
        in_string: int = False
        backslash_count: int = 0
        for j, c in enumerate(line):
            if c == '"' and backslash_count % 2 == 0:
                in_string = False
            if c == '\\':
                backslash_count += 1
            else:
                backslash_count = 0
            if (c == '#' or line[j:j+2] == '//') and not in_string:
                    data_lines[i] = line[:j]
                    break
            if line[j:j+2] == '/*' and not in_string:
                for n in range(j, len(line)):
                    if line[n:n+2] == '*/':
                        data_lines[i] = line[:j] + line[n+2:]
                        break
        in_string = True
    data_clean: str = '\n'.join(data_lines)
    return data_clean

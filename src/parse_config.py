import sys
try:
    from pathlib import Path
    import argparse
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()


def valid_type_file(p: Path) -> Path:

    if not p.is_file():
        raise ValueError(f'The path to the {p} file does not exist')
    if p.suffix != '.json':
        raise ValueError(f'{p}: Incorrect file format')
    return p


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Pac-Man game")
    parser.add_argument('config', help="path to JSON config file")
    return parser.parse_args()

import sys
from src.utils import COLORS
try:
    from pathlib import Path
    import argparse
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()


def valid_type_file(p: Path) -> Path:

    if not p.is_file():
        raise ValueError(f'Valide_type_file -> The path to the {p} file'
                         f' does not exist')
    if p.suffix != '.json':
        raise ValueError(f'Valide_type_file -> "{p}" is not a valid JSON file')
    return p


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Pac-Man game")
    parser.add_argument('config', help="path to JSON config file")
    return parser.parse_args()

import sys

from src.colors import COLORS

try:
    import argparse
    from pathlib import Path
except ImportError as e:
    print(f"{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}")
    sys.exit()


def valid_type_file(p: Path) -> Path:

    if not p.is_file():
        raise ValueError(
            f"Valide_type_file -> The path to the {p} file does not exist"
        )
    if p.suffix != ".json":
        raise ValueError(f'Valide_type_file -> "{p}" is not a valid JSON file')
    return p


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Pac-Man GameRender")
    parser.add_argument("config", help="path to JSON config file")
    return parser.parse_args()

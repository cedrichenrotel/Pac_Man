import sys
from src.colors import COLORS
try:
    from src.engine.model import UserScore
    from pydantic import ValidationError
    import os
    import json
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

    parser = argparse.ArgumentParser(description="Pac-Man GameRender")
    parser.add_argument('config', help="path to JSON config file")
    return parser.parse_args()


def parse_highscore(file: Path, path: str) -> bool:

    try:
        if os.stat(file).st_size != 0:
            with open(path) as f:
                data = json.load(f)
            for key, value in data.items():
                UserScore({key: value})

    except json.JSONDecodeError as e:
        print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
              f"Invalid highscore.json: {e}")
        return False
    except ValidationError:
        print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
              "parsing error in highscore.json: "
              "invalid format in {player_name : score}")
        return False

    return True

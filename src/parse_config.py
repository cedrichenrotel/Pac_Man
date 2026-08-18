import sys
try:
    from pathlib import Path
    from typing import Any
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

def parse_args()->argparse.Namespace: # classe fournie par argparse dont le seul but est de stocker des valeurs sous forme d'attributs, pour que tu puisses écrire args.config plutôt que args["config"].

    parser = argparse.ArgumentParser(description="Pac-Man game") # permet de donner des precision via: ' uv run python -m src --help'
    parser.add_argument('config', help="path to JSON config file") # 'config'permet d'attendre un arg sans avoir besoin d ajouter un flag(--config)

    return parser.parse_args()

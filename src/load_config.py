import sys
try:
    from pathlib import Path
    from typing import Any
    from src.utils import check_comments
    import json
except ImportError:
    sys.exit()

def read_json(file: Path | str) -> str:

    with open(file, 'r') as f:
        text: str = f.read()
        data: str = check_comments(text)
    return (data)

def load_json(file: Path | str) -> Any:

    with open(file, 'r') as f:
        data = json.load(f)
    return data


def create_json(file: Path, data: list[dict[str, Any]]) -> None:

    Path(file).parent.mkdir(parents=True, exist_ok=True)

    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

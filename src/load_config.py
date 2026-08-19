import sys
try:
    from pathlib import Path
    from typing import Any
    import json
except ImportError:
    sys.exit()


def load_json(file: Path | str) -> Any:

    with open(file, 'r') as f:
        data = json.load(f)

    return data


def create_json(file: Path, data: list[dict[str, Any]]) -> None:

    Path(file).parent.mkdir(parents=True, exist_ok=True)

    with open(file, 'w') as f:
        json.dump(data, f, indent=4)
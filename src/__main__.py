import sys
try:
    from src.error import ParseError
    from src.parse_config import parse_args, valid_type_file
    from src.load_config import load_json, read_json
    from src.model import Config_json, Level
    from typing import Any
    from pathlib import Path
    import argparse
#	from pydantic import ValidationError
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()


def main()->None:

    try:
        args: argparse.Namespace = parse_args()

        try:
            config_path: Path = valid_type_file(Path(args.config))
            clean_config_json: str = read_json(config_path)
            load_config_json: dict[str, Any] = load_json(clean_config_json)
        except Exception as e:
            print(f"[ERROR]: {e}")
            sys.exit()

        try:
            config: Config_json = Config_json(**load_config_json)
        except Exception as e:
            print(f"[WARNING] Invalid config values: {e}")

    except KeyboardInterrupt:
        print("[WARNING]: The programme was stopped manually")
        sys.exit()
    return


if __name__ == "__main__":
    main()

import sys
from src.colors import COLORS

try:
    # from src.render.GameRender import GameRender
    # from src.engine.init_maze import InitMaze
    from src.error import GameError
    from src.engine.parse_config import parse_args, valid_type_file
    from src.engine.load_config import load_json, read_json
    from src.engine.model import Config_json
    from src.engine.game_engine import GameEngine
    # from mazegenerator import MazeGenerator
    from typing import Any
    from pathlib import Path
    import argparse
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]:{COLORS['reset']} {e}')
    sys.exit()


def main() -> None:
    try:
        args: argparse.Namespace = parse_args()

        try:
            config_path: Path = valid_type_file(Path(args.config))
            clean_config_json: str = read_json(config_path)
            load_config_json: dict[str, Any] = load_json(clean_config_json)
        except Exception as e:
            print(f"{COLORS['bright_red']}[ERROR]:{COLORS['reset']} {e}")
            sys.exit()

        try:
            config: Config_json = Config_json(**load_config_json)
        except Exception as e:
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  f"Invalid config values: {e}")

        engine = GameEngine(config)
        engine.run()

    except (Exception, KeyboardInterrupt) as e:
        print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
              "The program was stopped manually")
        if isinstance(e, GameError):
            print(e)
        sys.exit()


if __name__ == "__main__":
    main()

import sys
from src.utils import COLORS

try:
    from src.game import Game
    from src.init_maze import RenderMaze
    from src.error import GameError
    from src.parse_config import parse_args, valid_type_file
    from src.load_config import load_json, read_json
    from src.model import Config_json
    from mazegenerator import MazeGenerator
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

        generator = MazeGenerator(
            size=(config.level[0].width, config.level[0].height),
            seed=config.seed
            )

        render_maze: RenderMaze = RenderMaze(generator, config)
        render_maze.config_start()
        game = Game(1000, 1000)
        game.run()

    except (Exception, KeyboardInterrupt) as e:
        print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
              "The program was stopped manually")
        if isinstance(e, GameError):
            print(e)
        sys.exit()


if __name__ == "__main__":
    main()

import sys
try:
    from src.game import Game
    from src.parse_config import parse_args, valid_type_file
    from src.load_config import load_json
    from pathlib import Path
    import argparse
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()


def main() -> None:
    try:
        args: argparse.Namespace = parse_args()

        try:
            config_path: Path = valid_type_file(Path(args.config))
            parse_config_json = load_json(config_path)
        except Exception as e:
            print(f"[ERROR]: {e}")
            sys.exit()

        try:
            config = Config_json(**parse_config_json)
        except Exception as e:
            print(f"[WARNING] Invalid config values: {e}")

    except KeyboardInterrupt:
        print("[WARNING]: The programme was stopped manually")
        sys.exit()
    # rajouter cette partir pour lancer le jeu 
    game = Game(1000, 1000)
    game.run()


if __name__ == "__main__":
    main()

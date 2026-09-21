import sys
import subprocess
import os
from src.colors import COLORS


def main() -> None:
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

        if os.path.exists(config_file):
            print("Configuration file found. Launching package via UV...")
            cmd = ["uv", "run", "python", "-m", "src", config_file]

            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"{COLORS['bright_red']}[ERROR]:{COLORS['reset']}"
                      f" Package execution failed: {e}")
                sys.exit(1)
            except FileNotFoundError:
                print(f"{COLORS['bright_red']}[ERROR]:{COLORS['reset']} 'uv'"
                      " tool is not installed or not found in PATH.")
                sys.exit(1)
        else:
            print(f"{COLORS['bright_red']}[ERROR]:{COLORS['reset']} "
                  f"File '{config_file}' does not exist.")
            sys.exit(1)

    else:
        print(f"{COLORS['bright_red']}[ERROR]:{COLORS['reset']}"
              " Missing arguments after the python file. "
              "Example: python3 pac-man.py config.json")
        sys.exit(1)


if __name__ == "__main__":
    main()

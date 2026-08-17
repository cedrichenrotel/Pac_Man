import sys
try:
	from typing import Any
	import argparse
#	from pydantic import ValidationError
except ImportError as e:
	print(f'[IMPORT ERROR]: {e}')
	sys.exit()


def parse_args()->argparse.Namespace: # classe fournie par argparse dont le seul but est de stocker des valeurs sous forme d'attributs, pour que tu puisses écrire args.config plutôt que args["config"].

	parser = argparse.ArgumentParser(description="Pac-Man game") # permet de donner des precision via: ' uv run python -m src --help'
	parser.add_argument('config', help="path to JSON config file") # 'config'permet d'attendre un arg sans avoir besoin d ajouter un flag(--config)
	return parser.parse_args()


def main()->None:

	args = parse_args()
	print("config file", args.config)
	return


if  __name__ == "__main__":
	main()
 
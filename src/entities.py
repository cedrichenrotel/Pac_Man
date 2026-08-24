import sys
try:
    from src.error import ParseError
    from src.model import Config_json
except ImportError as e:
    print(f'[IMPORT ERROR]: {e}')
    sys.exit()

class Entities:
    def __init__(self)
import sys
from src.utils import COLORS
try:
    from src.error import ParseError
    from src.model import Config_json
except ImportError as e:
    print(f'{COLORS['bright_red']}[IMPORT ERROR]{COLORS['reset']} {e}')
    sys.exit()

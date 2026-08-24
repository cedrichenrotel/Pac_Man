from src.utils import COLORS


class ParseError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"{COLORS['bright_red']}[PARSING_ERROR]"
                         f"{COLORS['reset']} "
                         f"{message}")


class GameError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"{COLORS['bright_red']}[ERROR]{COLORS['reset']} "
                         f"{message}")

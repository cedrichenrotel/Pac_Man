import sys

from src.colors import COLORS

try:
    import json
    import os
    from typing import Any
    from pathlib import Path
    from pydantic import (BaseModel, Field,
                          RootModel, model_validator,
                          ValidationError)
except ImportError:
    sys.exit()

UserScore = RootModel[dict[str, int]]


class Level(BaseModel):
    width: int = Field(default=15)
    height: int = Field(default=15)

    @model_validator(mode="before")
    def check_dimensions(cls, values: dict[str, Any]) -> dict[str, Any]:
        """checks that the dimensions of the maze are correct for the
        display"""

        if (
            not isinstance(values.get("width"), int)
            or values.get("width", 0) < 15
        ):
            values["width"] = 15
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "width too short, using min."
            )

        if (
            isinstance(values.get("width"), int)
            and values.get("width", 0) > 40
        ):
            values["width"] = 40
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "width too high, using max."
            )

        if (
            not isinstance(values.get("height"), int)
            or values.get("height", 0) < 15
        ):
            values["height"] = 15
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "height too short, using min."
            )

        if (
            isinstance(values.get("height"), int)
            and values.get("height", 0) > 20
        ):
            values["height"] = 20
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "height too high, using max."
            )

        return values


class Config_json(BaseModel):
    """Configuration model for the Pac-Man GameRender."""

    highscore_filename: str = Field(default="highscore.json")
    lives: int = Field(default=3)
    pacgum: int = Field(default=42)
    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=50)
    points_per_ghost: int = Field(default=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90)
    level: Level = Field(default_factory=Level)

    @staticmethod
    def parse_highscore(file: Path, path: str) -> bool:
        """check if highscore.json is in good format"""
        try:
            if os.stat(file).st_size != 0:
                with open(path) as f:
                    data = json.load(f)
                    if isinstance(data, dict) is False:
                        raise ValueError("format is not in {}")
                for key, value in data.items():
                    UserScore({key: value})
        except (json.JSONDecodeError, Exception)as e:
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                f"Invalid highscore.json: {e}"
            )
            return False
        except ValidationError:
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "parsing error in highscore.json: "
                "invalid format in {player_name : score}"
            )
            return False
        return True

    @model_validator(mode="before")
    def check_config_values(cls, values: dict[str, Any]) -> dict[str, Any]:

        if (
            not isinstance(values.get("highscore_filename"), str)
            or values.get("highscore_filename", str) == ""
        ):
            values["highscore_filename"] = "highscore.json"
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "invalid highscore_filename, using default."
            )
        else:
            if (cls.parse_highscore(Path(values["highscore_filename"]),
                                    values["highscore_filename"])
               is False):
                values["highscore_filename"] = "highscore.json"
                print(
                    f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                    "invalid highscore_filename, using default.")
        if (
            not isinstance(values.get("lives"), int)
            or values.get("lives", int) <= 0
            or values.get("lives", int) > 30
        ):
            values["lives"] = 3
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "invalid lives, using default."
            )

        level: Any | None = values.get("level")
        if not isinstance(level, dict):
            level = values["level"] = {"width": 15, "height": 15}
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "Invalid level value, using default."
            )
        val_width: Any = level.get("width")
        val_height: Any = level.get("height")

        if not isinstance(val_width, int):
            val_width = 15
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                f"Invalid width value, using default -> width: {val_width}."
            )
        if not isinstance(val_height, int):
            val_height = 15
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                f"Invalid height value, using default -> height: {val_height}."
            )

        if (
            not isinstance(values.get("pacgum"), int)
            or values.get("pacgum", int) < 0
            or values.get("pacgum", int) > (val_width * val_height) - 40
        ):
            values["pacgum"] = 42
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "invalid pacgum, using default."
            )

        if (
            not isinstance(values.get("points_per_pacgum"), int)
            or values.get("points_per_pacgum", int) < 0
            or values.get("points_per_pacgum", int) > 100
        ):
            values["points_per_pacgum"] = 10
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "Invalid points_per_pacgum, using default."
            )

        if (
            not isinstance(values.get("points_per_super_pacgum"), int)
            or values.get("points_per_super_pacgum", int) < 0
            or values.get("points_per_super_pacgum", int) > 500
        ):
            values["points_per_super_pacgum"] = 50
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "Invalid points_per_super_pacgum, using default."
            )

        if (
            not isinstance(values.get("points_per_ghost"), int)
            or values.get("points_per_ghost", int) < 0
            or values.get("points_per_ghost", int) > 1000
        ):
            values["points_per_ghost"] = 200
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "Invalid points_per_ghost, using default."
            )

        if (
            not isinstance(values.get("seed"), int)
            or values.get("seed", int) != 42
        ):
            values["seed"] = 42
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "Invalid seed, using default."
            )

        if (
            not isinstance(values.get("level_max_time"), int)
            or values.get("level_max_time", int) < 0
            or values.get("level_max_time", int) > 300
        ):
            values["level_max_time"] = 90
            print(
                f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                "Invalid level_max_time, using default."
            )

        return values

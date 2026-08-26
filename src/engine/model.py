import sys
from src.colors import COLORS
try:
    from typing import Any
    from pydantic import BaseModel, model_validator, Field
except ImportError:
    sys.exit()


class Level(BaseModel):

    width: int = Field(default=15)
    height: int = Field(default=15)

    @model_validator(mode="before")
    def check_dimensions(cls, values: dict[str, Any]) -> dict[str, Any]:
        if (not isinstance(values.get("width"), int) or
                values.get("width", 0) < 15):
            values["width"] = 15
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "invalid width, using default.")

        if (not isinstance(values.get("height"), int) or
                values.get("height", 0) < 15):
            values["height"] = 15
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "invalid height, using default.")
        return values


class Config_json(BaseModel):
    """Configuration model for the Pac-Man game."""

    highscore_filename: str = Field(default="highscore.json")
    lives: int = Field(default=3)
    pacgum: int = Field(default=42)
    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=50)
    points_per_ghost: int = Field(default=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90)
    level: list[Level] = Field(default_factory=list)

    @model_validator(mode="before")
    def check_config_values(cls, values: dict[str, Any]) -> dict[str, Any]:

        if (not isinstance(values.get("highscore_filename"), str) or
                values.get("highscore_filename", str) == ""):
            values["highscore_filename"] = "highscore.json"
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "invalid highscore_filename, using default.")

        if (not isinstance(values.get("lives"), int) or
                values.get("lives", int) <= 0):
            values["lives"] = 3
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "invalid lives, using default.")

        if (not isinstance(values.get("pacgum"), int) or
                values.get("pacgum", int) < 0):
            values["pacgum"] = 42
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "invalid pacgum, using default.")

        if (not isinstance(values.get("points_per_pacgum"), int) or
                values.get("points_per_pacgum", int) < 0):
            values["points_per_pacgum"] = 10
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "Invalid points_per_pacgum, using default.")

        if (not isinstance(values.get("points_per_super_pacgum"), int) or
                values.get("points_per_super_pacgum", int) < 0):
            values["points_per_super_pacgum"] = 50
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "Invalid points_per_super_pacgum, using default.")

        if (not isinstance(values.get("points_per_ghost"), int) or
                values.get("points_per_ghost", int) < 0):
            values["points_per_ghost"] = 200
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "Invalid points_per_ghost, using default.")

        if (not isinstance(values.get("seed"), int) or
                values.get("seed", int) < 0):
            values["seed"] = 42
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "Invalid seed, using default.")

        if (not isinstance(values.get("level_max_time"), int) or
                values.get("level_max_time", int) < 0):
            values["level_max_time"] = 90
            print(f"{COLORS['bright_yellow']}[WARNING]{COLORS['reset']} "
                  "Invalid level_max_time, using default.")

        if (not isinstance(values.get("level"), list) or
                len(values.get("level", [])) == 0):
            values["level"] = [{"width": 15, "height": 15}]
            print("[WARNING] Invalid level, using default.")

        return values

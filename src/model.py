import sys
try:
    from pydantic import BaseModel, model_validator, Field
    from typing import Any
except ImportError:
    sys.exit()


class Level(BaseModel):

    width: int = Field(default=15)
    height: int = Field(default=15)

    @model_validator(mode="before")
    def check_dimensions(cls, values):
        if values.get("width", 0) <= 2 or not isinstance("width", int):
            print(f"[WARNING] invalid width, using default")
            width = 15
        
        if values.get("height", 0) <= 2 or not isinstance("height", int):
            print(f"[WARNING] invalid height, using default")
            height = 15
        return values


class Config_json(BaseModel):

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
    def check_config_values(cls, values):

        if values.get("highscore_filename", str) == "" or not isinstance("highscore_filename", str):
            print(f"[WARNING] invalid highscore_filename, using default")
            values["highscore_filename"] = "highscore.json"
        if values.get("lives", int) <= 0 or not isinstance("lives", int):
            print(f"[WARNING] invalid lives, using default")
            values["lives"] = 3
        if values.get("pacgum", int) < 0 or not isinstance("pacgum", int):
            print(f"[WARNING] invalid pacgum, using default")
            values["pacgum"] = 42
        if values.get("points_per_pacgum", int) < 0 or not isinstance("points_per_pacgum", int):
            print(f"[WARNING] invalid points_per_pacgum, using default")
            values["points_per_pacgum"] = 42
        if values.get("points_per_super_pacgum", int) < 0 or not isinstance("points_per_super_pacgum", int):
            print(f"[WARNING] invalid points_per_super_pacgum, using default")
            values["points_per_super_pacgum"] = 50
        if values.get("points_per_ghost", int) < 0 or not isinstance("points_per_ghost", int):
            print(f"[WARNING] invalid points_per_ghost, using default")
            values["points_per_ghost"] = 200
        if values.get("seed", int) < 0 or not isinstance("seed", int):
            print(f"[WARNING] invalid seed, using default")
            values["seed"] = 42
        if values.get("level_max_time", int) < 0 or not isinstance("level_max_time", int):
            print(f"[WARNING] invalid , using default")
            values["level_max_time"] = 90
        return values
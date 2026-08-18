import sys
try:
    from pydantic import BaseModel, model_validator
    from typing import Any
except ImportError:
    sys.exit()


class Config_json(BaseModel):
    highscore_filename: str
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int

class Level(BaseModel):
    width: int
    height: int
from pydantic import Field

from files.models.frameworks.FrameWork import FrameWork


class Level(FrameWork):
    level:float
    fib_level:float
    typ: str = Field(default='Level')
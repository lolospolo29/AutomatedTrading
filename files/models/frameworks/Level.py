from pydantic import Field

from files.models.frameworks.FrameWork import FrameWork


class Level(FrameWork):
    level:float = Field(exclude=True)
    fib_level:float = Field(exclude=True)
    typ: str = Field(default='Level',exclude=True)
from pydantic import Field

from files.models.frameworks.FrameWork import FrameWork


class Structure(FrameWork):
    typ: str = Field(default='Structure')

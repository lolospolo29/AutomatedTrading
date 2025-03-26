from pydantic import Field

from files.models.frameworks.FrameWork import FrameWork


class PDArray(FrameWork):
    typ: str = Field(default='PDArray',exclude=True)

from enum import Enum


class OpenOnlyEnum(Enum):
    DEFAULT = 0
    EXCEPTINVERSE = 1
    INVERSE = 2
    OPENONLY = "openOnly"



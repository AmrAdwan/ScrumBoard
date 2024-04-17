from enum import Enum

class rights(Enum):
    VIEW = 1
    DRAG = 2
    CLAIM = 3
    EDIT = 4
    CREATE = 5
    ALL = 6

class status(Enum):
    BACKLOG = 1
    READY = 2
    PROGRESS = 3
    REVIEW = 4
    DONE = 5
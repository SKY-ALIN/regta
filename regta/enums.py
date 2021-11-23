from enum import Enum


class JobTypes(Enum):
    ASYNC = 'async'
    THREAD = 'thread'
    PROCESS = 'process'

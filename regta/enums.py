from enum import Enum


class JobTypes(Enum):
    ASYNC = 'async'
    THREAD = 'thread'
    PROCESS = 'process'


class DecoratorNames(Enum):
    async_job = JobTypes.ASYNC
    thread_job = JobTypes.THREAD
    process_job = JobTypes.PROCESS


class CodeStyles(Enum):
    OOP = 'oop'
    DECORATOR = 'decorator'

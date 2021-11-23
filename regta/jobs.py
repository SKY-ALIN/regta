from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Callable, Union, Type
from threading import Thread, Event as ThreadEvent
from multiprocessing import Process, Event as ProcessEvent


class AbstractJob(ABC):
    INTERVAL: timedelta = NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    def execute(self):
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError


@dataclass
class JobData:
    interval: timedelta = None
    execute: Callable = None
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)


class BaseSyncJob(AbstractJob):
    BLOCKER_CLASS: Type[Union[ThreadEvent, ProcessEvent]]
    INTERVAL: timedelta = None

    def __init__(self, **kwargs):
        self.data = JobData(**kwargs)
        self.interval = self.data.interval or self.INTERVAL
        self.blocker = self.BLOCKER_CLASS()

    def run(self):
        execute = self.data.execute or self.execute
        while not self.blocker.wait(self.interval.total_seconds()):
            execute(*self.data.args, **self.data.kwargs)


class ProcessJob(BaseSyncJob, Process):
    BLOCKER_CLASS = ProcessEvent

    def __init__(self, **kwargs):
        Process.__init__(self)
        super(ProcessJob, self).__init__(**kwargs)

    def stop(self):
        self.blocker.set()
        self.join()
        self.terminate()


class ThreadJob(BaseSyncJob, Thread):
    BLOCKER_CLASS = ThreadEvent

    def __init__(self, **kwargs):
        Thread.__init__(self)
        super(ThreadJob, self).__init__(**kwargs)

    def stop(self):
        self.blocker.set()
        self.join()


class AsyncJob(AbstractJob):
    async def stop(self): pass
    async def run(self): pass

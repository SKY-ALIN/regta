from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Callable, Union, Type
from threading import Thread, Event as ThreadEvent
from multiprocessing import Process, Event as ProcessEvent

from .enums import JobTypes


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


class BaseJob(AbstractJob):
    INTERVAL: timedelta = None

    def __init__(self, **kwargs):
        self.data = JobData(**kwargs)
        self.interval = self.data.interval or self.INTERVAL
        if self.interval is None:
            raise ValueError("Interval is not specified")
        self.execute = self.data.execute or self.execute
        if self.execute is None:
            raise ValueError("Execute is not specified")

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError


class BaseSyncJob(BaseJob):
    BLOCKER_CLASS: Type[Union[ThreadEvent, ProcessEvent]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocker = self.BLOCKER_CLASS()

    def _execute(self):
        self.execute(*self.data.args, **self.data.kwargs)

    def run(self):
        self._execute()
        while not self.blocker.wait(self.interval.total_seconds()):
            self._execute()

    @abstractmethod
    def stop(self):
        raise NotImplementedError


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


class AsyncJob(BaseJob):
    async def _execute(self):
        await self.execute(*self.data.args, **self.data.kwargs)

    async def run(self):
        while True:
            await self._execute()
            await asyncio.sleep(self.interval.total_seconds())

    async def stop(self): pass


jobs_classes = {
    JobTypes.ASYNC: AsyncJob,
    JobTypes.THREAD: ThreadJob,
    JobTypes.PROCESS: ProcessJob,
}

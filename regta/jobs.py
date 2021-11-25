from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Callable, Union, Type
import traceback
from threading import Thread, Event as ThreadEvent
from multiprocessing import Process, Event as ProcessEvent

import click

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


def show_exception(job, e: Exception):
    click.echo(
        f"{click.style(job, fg='blue')} - " +
        f"{click.style(f'{e.__class__.__name__}: {str(e)}', fg='red')}\n" +
        click.style("".join(traceback.format_tb(e.__traceback__)), fg='yellow')
    )


def show_result(job, res: str):
    click.echo(f"{click.style(job, fg='blue')} - {res}")


class BaseJob(AbstractJob):
    INTERVAL: timedelta = None
    execute: Callable = None

    def __init__(self, **kwargs):
        self.data = JobData(**kwargs)
        self.interval = self.data.interval or self.INTERVAL
        if self.interval is None:
            raise ValueError("Interval is not specified")
        self.execute = self.data.execute or self.execute
        if self.execute is None:
            raise ValueError("Execute is not specified")

    def _log_error(self, e: Exception):
        show_exception(self, e)

    def _log_result(self, res: str):
        show_result(self, str(res))

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    def __str__(self):
        return f"{self.__module__}:{self.__class__.__name__}"


class BaseSyncJob(BaseJob):
    BLOCKER_CLASS: Type[Union[ThreadEvent, ProcessEvent]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocker = self.BLOCKER_CLASS()

    def _execute(self):
        try:
            res = self.execute(*self.data.args, **self.data.kwargs)
            self._log_result(res)
        except Exception as e:
            self._log_error(e)

    def __block(self):
        try:
            return self.blocker.wait(self.interval.total_seconds())
        except KeyboardInterrupt:
            pass
        return True

    def run(self):
        self._execute()
        while not self.__block():
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
        try:
            res = await self.execute(*self.data.args, **self.data.kwargs)
            self._log_result(res)
        except Exception as e:
            self._log_error(e)

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

JobHint = Union[AsyncJob, ThreadJob, ProcessJob]

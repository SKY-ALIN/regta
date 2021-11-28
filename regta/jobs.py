from abc import ABC, abstractmethod
import asyncio
from datetime import timedelta
from typing import Callable, Union, Type, Iterable
import traceback
from threading import Thread, Event as ThreadEvent
from multiprocessing import Process, Event as ProcessEvent
from logging import Logger

import click

from .enums import JobTypes


class AbstractJob(ABC):
    interval: timedelta = NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    def execute(self):
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError


def show_exception(job, e: Exception, logger: Logger = None):
    if logger is None:
        click.echo(
            f"{job.styled_str()} - " +
            f"{click.style(f'{e.__class__.__name__}: {str(e)}', fg='red')}\n" +
            click.style("".join(traceback.format_tb(e.__traceback__)), fg='yellow')
        )
    else:
        logger.error(
            f"{job} - " +
            f"{e.__class__.__name__}: {str(e)}\n" +
            "".join(traceback.format_tb(e.__traceback__))
        )


def show_result(job, res: str, logger: Logger = None):
    if logger is None:
        click.echo(f"{job.styled_str()} - {res}")
    else:
        logger.info(f"{job} - {res}")


class BaseJob(AbstractJob):
    interval: timedelta = None
    execute: Callable = None
    logger: Logger = None
    args: Iterable = []
    kwargs: dict = {}

    def __init__(self, *args, interval: timedelta = None, execute: Callable = None, logger: Logger = None, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.interval = interval or self.interval
        if self.interval is None:
            raise ValueError("Interval is not specified")
        self.execute = execute or self.execute
        if self.execute is None:
            raise ValueError("Execute is not specified")
        self.logger = logger or self.logger

    def _log_error(self, e: Exception):
        if self.logger is not None:
            self.logger.error(
                f"{self} - " +
                f"{e.__class__.__name__}: {str(e)}\n" +
                "".join(traceback.format_tb(e.__traceback__))
            )
        else:
            click.echo(
                f"{self.styled_str()} - " +
                f"{click.style(f'{e.__class__.__name__}: {str(e)}', fg='red')}\n" +
                click.style("".join(traceback.format_tb(e.__traceback__)), fg='yellow')
            )

    def _log_result(self, res: str):
        if self.logger is not None:
            self.logger.info(f"{self} - {res}")
        else:
            click.echo(f"{self.styled_str()} - {res}")

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @classmethod
    def __str__(cls):
        return f"{cls.__module__}:{cls.__name__}"

    @classmethod
    def styled_str(cls):
        return f"{cls.__module__}:{click.style(cls.__name__, fg='blue')}"


class BaseSyncJob(BaseJob):
    BLOCKER_CLASS: Type[Union[ThreadEvent, ProcessEvent]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocker = self.BLOCKER_CLASS()

    def _execute(self):
        try:
            res = self.execute(*self.args, **self.kwargs)
            self._log_result(res)
        except Exception as e:  # pylint: disable=broad-except
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
        super().__init__(**kwargs)

    def stop(self):
        self.blocker.set()
        self.join()
        self.terminate()


class ThreadJob(BaseSyncJob, Thread):
    BLOCKER_CLASS = ThreadEvent

    def __init__(self, **kwargs):
        Thread.__init__(self)
        super().__init__(**kwargs)

    def stop(self):
        self.blocker.set()
        self.join()


class AsyncJob(BaseJob):
    async def _execute(self):
        try:
            res = await self.execute(*self.args, **self.kwargs)
            self._log_result(res)
        except Exception as e:  # pylint: disable=broad-except
            self._log_error(e)

    async def run(self):
        while True:
            await self._execute()
            await asyncio.sleep(self.interval.total_seconds())

    async def stop(self): pass


JobHint = Union[AsyncJob, ThreadJob, ProcessJob]


def _make_decorator(_class: Type[JobHint]):
    def decorator(interval: timedelta, *args, **kwargs):
        def wrapper(func: Callable):
            return type(
                func.__name__,
                (_class,),
                {
                    "__module__": func.__module__,
                    "execute": staticmethod(func),
                    "interval": interval,
                    "args": args,
                    "kwargs": kwargs,
                }
            )
        return wrapper
    return decorator


async_job = _make_decorator(AsyncJob)
thread_job = _make_decorator(ThreadJob)
process_job = _make_decorator(ProcessJob)

jobs_classes = {
    JobTypes.ASYNC: AsyncJob,
    JobTypes.THREAD: ThreadJob,
    JobTypes.PROCESS: ProcessJob,
}

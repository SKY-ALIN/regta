"""Contains bases of different job types.

You can use the following entities to build your jobs:
    * Class :class:`AsyncJob` or :class:`async_job` decorator
    * Class :class:`ThreadJob` or :class:`thread_job` decorator
    * Class :class:`ProcessJob` or :class:`process_job` decorator
"""

from abc import ABC, abstractmethod
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Awaitable, Callable, Union, Type, Iterable
from threading import Thread, Event as ThreadEvent
from multiprocessing import Process, Event as ProcessEvent
from logging import Logger, LoggerAdapter

import click
from regta_period import AbstractPeriod

from .enums import JobTypes
from .logging import JobLoggerAdapter, make_default_logger


class AbstractJob(ABC):
    """Interface which every job base implement."""

    interval: Union[timedelta, AbstractPeriod] = NotImplemented
    """A timedelta object which describe interval between every
    :meth:`.execute` call.
    """

    @abstractmethod
    def stop(self):
        """Method will be called by the scheduler when regta gets stop
        signal.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        """The function on which job will be based. Must be rewritten.
        It'll be called every :attr:`.interval`.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self):
        """Method will be called by scheduler when regta starts. It'll
        call :meth:`.execute` every :attr:`.interval`.
        """
        raise NotImplementedError


class BaseJob(AbstractJob):
    """Base job class which implements common logic."""

    interval: Union[timedelta, AbstractPeriod, None] = None
    """A timedelta object which describe interval between every
    :attr:`.execute` call.
    """
    execute: Union[Callable, None] = None
    """The function on which job will be based. Must be rewritten or passed.
    It'll be called every :attr:`.interval`.
    """
    logger: Union[Logger, LoggerAdapter, None] = None
    """Logger writes all results of :attr:`.execute` function and
    its exceptions. If the logger isn't specified, regta will use std output.
    """
    args: Iterable = []
    """Args will be passed into :attr:`.execute`."""
    kwargs: dict = {}
    """Key-word args will be passed into :attr:`.execute`."""

    def __init__(
            self,
            *args,
            interval: Union[timedelta, AbstractPeriod, None] = None,
            execute: Union[Callable, None] = None,
            logger: Union[Logger, None] = None,
            **kwargs,
    ):
        self.args = args
        self.kwargs = kwargs

        self.interval = interval or self.interval
        if self.interval is None:
            raise ValueError("Interval is not specified")

        self.execute = execute or self.execute
        if self.execute is None:
            raise ValueError("Execute is not specified")

        use_ansi: bool = (logger is None and self.logger is None)
        logger = logger or self.logger or make_default_logger(use_ansi=use_ansi)
        self.logger = JobLoggerAdapter(logger, job=self, use_ansi=use_ansi)

    def _get_seconds_till_to_execute(self) -> float:
        if isinstance(self.interval, timedelta):
            return self.interval.total_seconds()
        if isinstance(self.interval, AbstractPeriod):
            if self.interval.is_timezone_in_use:
                current_moment = datetime.now(timezone.utc)
            else:
                current_moment = datetime.utcnow()
            return self.interval.get_interval(current_moment).total_seconds()
        raise ValueError(f"Regta doesn't support '{self.interval.__class__.__name__}' type for interval.")

    @abstractmethod
    def run(self):
        """Method will be called by scheduler when regta starts. It'll
        call :attr:`.execute` every :attr:`.interval`.
        """
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
    """Class contains common for :class:`ThreadJob` and
    :class:`ProcessJob` blocking.

    .. autoattribute:: interval
    .. autoattribute:: execute
    .. autoattribute:: logger
    .. autoattribute:: args
    .. autoattribute:: kwargs
    """

    _blocker_class: Type[Union[ThreadEvent, ProcessEvent]]

    def __init__(
            self,
            *args,
            interval: Union[timedelta, AbstractPeriod, None] = None,
            execute: Union[Callable, None] = None,
            logger: Union[Logger, None] = None,
            **kwargs,
    ):
        super().__init__(*args, interval=interval, execute=execute, logger=logger, **kwargs)
        self._blocker = self._blocker_class()

    def _execute(self):
        try:
            res = self.execute(*self.args, **self.kwargs)
            self.logger.info(res)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.exception(e)

    def __block(self):
        try:
            return self._blocker.wait(self._get_seconds_till_to_execute())
        except KeyboardInterrupt:
            pass
        return True

    def run(self):
        while not self.__block():
            self._execute()

    @abstractmethod
    def stop(self):
        raise NotImplementedError


class ProcessJob(BaseSyncJob, Process):
    """Sync job class based on a process.

    .. autoattribute:: interval
    .. autoattribute:: execute
    .. autoattribute:: logger
    .. autoattribute:: args
    .. autoattribute:: kwargs
    .. automethod:: regta.ProcessJob.run
    """

    _blocker_class = ProcessEvent

    def __init__(
            self,
            *args,
            interval: Union[timedelta, AbstractPeriod, None] = None,
            execute: Union[Callable, None] = None,
            logger: Union[Logger, None] = None,
            **kwargs,
    ):
        Process.__init__(self)
        super().__init__(*args, interval=interval, execute=execute, logger=logger, **kwargs)

    def stop(self):
        """Stops and terminates job's process. It will be called by the scheduler
        when regta gets a stop signal.
        """
        self._blocker.set()
        self.join()
        self.terminate()


class ThreadJob(BaseSyncJob, Thread):
    """Sync job class based on a thread.

    .. autoattribute:: interval
    .. autoattribute:: execute
    .. autoattribute:: logger
    .. autoattribute:: args
    .. autoattribute:: kwargs
    .. automethod:: regta.ThreadJob.run
    """

    _blocker_class = ThreadEvent

    def __init__(
            self,
            *args,
            interval: Union[timedelta, AbstractPeriod, None] = None,
            execute: Union[Callable, None] = None,
            logger: Union[Logger, None] = None,
            **kwargs,
    ):
        Thread.__init__(self)
        super().__init__(*args, interval=interval, execute=execute, logger=logger, **kwargs)

    def stop(self):
        """Stops job's thread. It will be called by the scheduler
        when regta gets a stop signal.
        """
        self._blocker.set()
        self.join()


class AsyncJob(BaseJob):
    """Async job class. Will be executed in an event loop.

    .. autoattribute:: interval
    .. autoattribute:: logger
    .. autoattribute:: args
    .. autoattribute:: kwargs
    """

    execute: Union[Callable[..., Awaitable[Union[str, None]]], None] = None
    """The async function on which job will be based. Must be rewritten or
    passed. It'll be called every :attr:`.interval`.
    """

    async def _execute(self):
        try:
            res = await self.execute(*self.args, **self.kwargs)
            self.logger.info(res)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.exception(e)

    async def run(self):
        while True:
            await self._execute()
            await asyncio.sleep(self._get_seconds_till_to_execute())

    async def stop(self): pass


JobHint = Union[AsyncJob, ThreadJob, ProcessJob]


def _make_decorator(_class: Type[JobHint]):
    def decorator(interval: Union[timedelta, AbstractPeriod], *args, **kwargs):
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
async_job.__doc__ = (
    """Decorator makes :class:`AsyncJob` from async function.

    Args:
        interval: A timedelta object which describes the interval between every call.
        *args: Will be passed into the function.
        **kwargs: Will be passed into the function.
    """
)
thread_job = _make_decorator(ThreadJob)
thread_job.__doc__ = (
    """Decorator makes :class:`ThreadJob` from function.

    Args:
        interval: A timedelta object which describes the interval between every call.
        *args: Will be passed into the function.
        **kwargs: Will be passed into the function.
    """
)
process_job = _make_decorator(ProcessJob)
process_job.__doc__ = (
    """Decorator makes :class:`ProcessJob` from function.

    Args:
        interval: A timedelta object which describes the interval between every call.
        *args: Will be passed into the function.
        **kwargs: Will be passed into the function.
    """
)

jobs_classes = {
    JobTypes.ASYNC: AsyncJob,
    JobTypes.THREAD: ThreadJob,
    JobTypes.PROCESS: ProcessJob,
}

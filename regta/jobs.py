"""Contains bases of different job types.

You can use the following entities to build your jobs:
    * Class :class:`AsyncJob` or :class:`regta.async_job` decorator
    * Class :class:`ThreadJob` or :class:`regta.thread_job` decorator
    * Class :class:`ProcessJob` or :class:`regta.process_job` decorator
"""

from typing import Awaitable, Callable, Dict, Iterable, Type, Union

from abc import ABC, abstractmethod
import asyncio
from datetime import datetime, timedelta, timezone
from logging import Logger, LoggerAdapter
from multiprocessing import Event as ProcessEventFabric, Process
from multiprocessing.synchronize import Event as ProcessEventObject
from threading import Event as ThreadEvent, Thread

import click
from regta_period import AbstractPeriod

from .enums import JobTypes
from .logging import JobLoggerAdapter, make_default_logger


class AbstractJob(ABC):
    """Interface which every job base implement."""

    interval: Union[timedelta, AbstractPeriod]
    """Interval between every :meth:`.func` call."""
    func: Callable[..., Union[str, None]]
    """The function on which the job will be based. Must be rewritten or passed.
    It'll be called every :attr:`.interval`.
    """

    @abstractmethod
    def execute(self):
        """Execute :attr:`.func` and log result/error.
        It will be called by the job every :attr:`.interval`.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self):
        """Method will be called by scheduler when regta starts. It'll
        call :attr:`.func` every :attr:`.interval`.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Method will be called by the scheduler when regta gets stop
        signal.
        """
        raise NotImplementedError


class BaseJob(AbstractJob):
    """Base job class which implements common logic."""

    interval: Union[timedelta, AbstractPeriod]
    """Interval between every :meth:`.func` call."""
    func: Callable[..., Union[str, None]]
    """The function on which job will be based. Must be rewritten or passed.
    It'll be called every :attr:`.interval`.
    """
    logger: Union[Logger, LoggerAdapter, None] = None
    """Logger writes all results of :attr:`.func` function and
    its exceptions. If the logger isn't specified, regta will use std output.
    """
    args: Iterable = []
    """Args will be passed into :attr:`.func`."""
    kwargs: dict = {}
    """Key-word args will be passed into :attr:`.func`."""

    def __init__(
            self,
            *args,
            logger: Union[Logger, None] = None,
            use_ansi: bool = True,
            **kwargs,
    ):
        self.args = args
        self.kwargs = kwargs

        _logger: Logger = self.logger or logger or make_default_logger(use_ansi=use_ansi)  # type: ignore
        self.logger = JobLoggerAdapter(
            _logger,
            plain_job_name=self.get_plain_job_name(),
            styled_job_name=self.get_styled_job_name(),
            use_ansi=use_ansi,
        )

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
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @classmethod
    def get_plain_job_name(cls):
        return f"{cls.__module__}:{cls.__name__}"

    @classmethod
    def get_styled_job_name(cls):
        return f"{cls.__module__}:{click.style(cls.__name__, fg='blue')}"


class BaseSyncJob(BaseJob):
    """Class contains common for :class:`ThreadJob` and
    :class:`ProcessJob` blocking.

    .. autoattribute:: interval
    .. autoattribute:: func
    .. autoattribute:: logger
    .. autoattribute:: args
    .. autoattribute:: kwargs
    """

    _blocker_class: Union[Type[ThreadEvent], Callable[..., ProcessEventObject]]

    def __init__(
            self,
            *args,
            logger: Union[Logger, None] = None,
            use_ansi: bool = True,
            **kwargs,
    ):
        super().__init__(*args, logger=logger, use_ansi=use_ansi, **kwargs)
        self._blocker = self._blocker_class()

    def execute(self):
        try:
            res = self.func(*self.args, **self.kwargs)
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
            self.execute()

    @abstractmethod
    def stop(self):
        raise NotImplementedError


class ProcessJob(BaseSyncJob, Process):
    """Sync job class based on a process.

    .. autoattribute:: interval
    .. autoattribute:: func
    .. autoattribute:: logger
    .. autoattribute:: args
    .. autoattribute:: kwargs
    .. automethod:: execute
    .. automethod:: run
    """

    _blocker_class = ProcessEventFabric

    def __init__(
            self,
            *args,
            logger: Union[Logger, None] = None,
            use_ansi: bool = True,
            **kwargs,
    ):
        Process.__init__(self)
        super().__init__(*args, logger=logger, use_ansi=use_ansi, **kwargs)

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
    .. autoattribute:: func
    .. autoattribute:: logger
    .. autoattribute:: args
    .. autoattribute:: kwargs
    .. automethod:: execute
    .. automethod:: run
    """

    _blocker_class = ThreadEvent

    def __init__(
            self,
            *args,
            logger: Union[Logger, None] = None,
            use_ansi: bool = True,
            **kwargs,
    ):
        Thread.__init__(self)
        super().__init__(*args, logger=logger, use_ansi=use_ansi, **kwargs)

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

    func: Callable[..., Awaitable[Union[str, None]]]  # type: ignore
    """The function on which the job will be based. Must be rewritten or passed.
    It'll be called every :attr:`.interval`.
    """

    async def execute(self):
        try:
            res = await self.func(*self.args, **self.kwargs)
            self.logger.info(res)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.exception(e)

    async def run(self):
        while True:
            await asyncio.sleep(self._get_seconds_till_to_execute())
            await self.execute()

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
                    "func": staticmethod(func),
                    "interval": interval,
                    "args": args,
                    "kwargs": kwargs,
                }
            )
        return wrapper
    return decorator


async_job = _make_decorator(AsyncJob)
async_job.__doc__ = (
    """Make :class:`AsyncJob` from async function.

    Args:
        interval: Interval between every call.
        *args: Will be passed into the function.
        **kwargs: Will be passed into the function.
    """
)
thread_job = _make_decorator(ThreadJob)
thread_job.__doc__ = (
    """Make :class:`ThreadJob` from function.

    Args:
        interval: Interval between every call.
        *args: Will be passed into the function.
        **kwargs: Will be passed into the function.
    """
)
process_job = _make_decorator(ProcessJob)
process_job.__doc__ = (
    """Make :class:`ProcessJob` from function.

    Args:
        interval: Interval between every call.
        *args: Will be passed into the function.
        **kwargs: Will be passed into the function.
    """
)

jobs_classes: Dict[JobTypes, Type[JobHint]] = {
    JobTypes.ASYNC: AsyncJob,
    JobTypes.THREAD: ThreadJob,
    JobTypes.PROCESS: ProcessJob,
}

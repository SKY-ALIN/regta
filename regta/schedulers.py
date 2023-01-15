"""Contains family of different schedulers.

Use following schedulers to build your system:
    * :class:`AsyncScheduler` for only :class:`regta.AsyncJob`.
    * :class:`SyncScheduler` for only sync jobs (:class:`regta.ThreadJob` or :class:`regta.ProcessJob`).
    * :class:`Scheduler` for all types of jobs (**recommended**).
"""

from typing import List, Union

from abc import ABC, abstractmethod
import asyncio
import signal
from threading import Thread
import time

from .exceptions import IncorrectJobType, StopService
from .jobs import AbstractJob, AsyncJob, ProcessJob, ThreadJob


class AbstractScheduler(ABC):
    """Interface which every scheduler implement."""

    @abstractmethod
    def add_job(self, job: AbstractJob):
        """Add job to scheduler jobs list which will be started.

        Args:
            job: The job will be added.

        Raises:
            IncorrectJobType: If incorrect job type will be passed.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self, block: bool = True):
        """Run scheduler's jobs.

        Args:
            block:
                If True, blocks the current thread. If False, the thread will
                not be blocked and your script will continue.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stops scheduler's jobs.

        Will be called by :class:`regta.schedulers.SyncBlocking` when regta
        gets stop signal (:exc:`SystemExit`, :exc:`KeyboardInterrupt`, etc.)
        or if the scheduler's thread is not blocked, you can call it yourself.
        """
        raise NotImplementedError


class SyncBlocking(AbstractScheduler, ABC):
    """Contains sync blocking code to add :code:`block` bool var to
    :meth:`.AbstractScheduler.run` to block thread.
    """

    __original_sigterm_handler = None
    __original_sigint_handler = None

    def __stop(self, sig, frame):  # pylint: disable=unused-argument
        self.stop()
        signal.signal(signal.SIGTERM, self.__original_sigterm_handler)
        signal.signal(signal.SIGINT, self.__original_sigint_handler)
        raise StopService

    def _block_main(self):
        self.__original_sigterm_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, self.__stop)
        self.__original_sigint_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.__stop)

        while True:
            try:
                time.sleep(1)
            except StopService:
                break


class SyncScheduler(SyncBlocking, AbstractScheduler):
    _thread_jobs: List[ThreadJob] = []
    _process_jobs: List[ProcessJob] = []

    def add_job(self, job: Union[ThreadJob, ProcessJob]):  # type: ignore[override]
        if isinstance(job, ThreadJob):
            self._thread_jobs.append(job)
        elif isinstance(job, ProcessJob):
            self._process_jobs.append(job)
        else:
            raise IncorrectJobType(job, self)

    @staticmethod
    def __start_jobs(jobs: Union[List[ThreadJob], List[ProcessJob]], block: bool):
        for job in jobs:
            job.daemon = not block
            job.start()

    def run(self, block: bool = True):
        self.__start_jobs(self._thread_jobs, block)
        self.__start_jobs(self._process_jobs, block)

        if block:
            self._block_main()

    @staticmethod
    def __stop_jobs(jobs: List[Union[ThreadJob, ProcessJob]]):
        for job in jobs:
            job.stop()

    def stop(self):
        self.__stop_jobs(self._thread_jobs)
        self.__stop_jobs(self._process_jobs)


class AsyncScheduler(AbstractScheduler, Thread):
    _async_jobs: List[AsyncJob] = []
    _async_tasks: List = []

    def __init__(self):
        Thread.__init__(self)
        super().__init__()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def add_job(self, job: AsyncJob):  # type: ignore[override]
        if isinstance(job, AsyncJob):
            self._async_jobs.append(job)
        else:
            raise IncorrectJobType(job, self)

    def run(self, block: bool = True):
        self._async_tasks = [
            self.loop.create_task(job.run())
            for job in self._async_jobs
        ]
        self.loop.run_forever()

    def stop(self):
        """Stop scheduler's jobs."""
        for task in self._async_tasks:
            task.cancel()
        self.loop.call_soon_threadsafe(self.loop.stop)


class Scheduler(SyncBlocking, AbstractScheduler):
    sync_scheduler: Union[SyncScheduler, None] = None
    async_scheduler: Union[AsyncScheduler, None] = None

    def add_job(self, job: Union[AsyncJob, ThreadJob, ProcessJob]):  # type: ignore[override]
        if isinstance(job, AsyncJob):
            if self.async_scheduler is None:
                self.async_scheduler = AsyncScheduler()
            self.async_scheduler.add_job(job)
        elif isinstance(job, (ThreadJob, ProcessJob)):
            if self.sync_scheduler is None:
                self.sync_scheduler = SyncScheduler()
            self.sync_scheduler.add_job(job)
        else:
            raise IncorrectJobType(job, self)

    def run(self, block: bool = True):
        if self.sync_scheduler is not None:
            self.sync_scheduler.run(block=(self.async_scheduler is None and block))
        if self.async_scheduler is not None:
            self.async_scheduler.daemon = not block
            self.async_scheduler.start()
        if block and self.async_scheduler is not None:
            self._block_main()

    def stop(self):
        if self.sync_scheduler is not None:
            self.sync_scheduler.stop()
        if self.async_scheduler is not None:
            self.async_scheduler.stop()

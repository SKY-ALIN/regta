from abc import ABC, abstractmethod
import asyncio
from typing import Union, List
from multiprocessing import Process
import signal
import time

from .jobs import AbstractJob, ProcessJob, ThreadJob, AsyncJob
from .exceptions import StopService, IncorrectJobType


class AbstractScheduler(ABC):
    @abstractmethod
    def add_job(self, job: AbstractJob):
        raise NotImplementedError

    @abstractmethod
    def run(self, block: bool):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError


class BaseScheduler(AbstractScheduler):
    pass


class SyncScheduler(BaseScheduler):
    thread_jobs: List[ThreadJob] = []
    process_jobs: List[ProcessJob] = []

    def add_job(self, job: Union[ThreadJob, ProcessJob]):
        if isinstance(job, ThreadJob):
            self.thread_jobs.append(job)
        elif isinstance(job, ProcessJob):
            self.process_jobs.append(job)
        else:
            raise IncorrectJobType(job, self)

    @staticmethod
    def __start_jobs(jobs: List[Union[ThreadJob, ProcessJob]], block: bool):
        for job in jobs:
            job.daemon = not block
            job.start()

    @staticmethod
    def __exit(signum, frame):
        raise StopService

    def __block_main(self):
        signal.signal(signal.SIGTERM, self.__exit)
        signal.signal(signal.SIGINT, self.__exit)

        while True:
            try:
                time.sleep(1)
            except StopService:
                self.stop()
                break

    def run(self, block: bool):
        self.__start_jobs(self.thread_jobs, block)
        self.__start_jobs(self.process_jobs, block)

        if block:
            self.__block_main()

    @staticmethod
    def __stop_jobs(jobs: List[Union[ThreadJob, ProcessJob]]):
        for job in jobs:
            job.stop()

    def stop(self):
        self.__stop_jobs(self.thread_jobs)
        self.__stop_jobs(self.process_jobs)


class AsyncScheduler(BaseScheduler, Process):
    async_jobs: List[AsyncJob] = []
    async_tasks: List = []

    def __init__(self):
        Process.__init__(self)
        super(AsyncScheduler, self).__init__()
        self.loop = asyncio.get_event_loop()

    def add_job(self, job: AsyncJob):
        if isinstance(job, AsyncJob):
            self.async_jobs.append(job)
        else:
            raise IncorrectJobType(job, self)

    def _run(self):
        self.async_tasks = [
            self.loop.create_task(job.run())
            for job in self.async_jobs
        ]
        self.loop.run_forever()

    def run(self, block: bool):
        self._run()

    def stop(self):
        for job in self.async_tasks:
            job.task.cancel()
        self.join()
        self.terminate()


class Scheduler(BaseScheduler):
    sync_scheduler: SyncScheduler = None
    async_scheduler: AsyncScheduler = None

    def add_job(self, job: Union[AsyncJob, ThreadJob, ProcessJob]):
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

    def run(self, block: bool):
        if self.sync_scheduler is not None:
            self.sync_scheduler.run(block=(self.async_scheduler is None and block))
        if self.async_scheduler is not None:
            self.async_scheduler.run(block=block)

    def stop(self): pass



from abc import ABC, abstractmethod
from typing import Union, List
from threading import Thread
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
    def start(self, block: bool):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError


class BaseScheduler(AbstractScheduler):
    pass


class AsyncScheduler(BaseScheduler):
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

    def start(self, block: bool):
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

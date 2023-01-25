=============
API Reference
=============

Main module API
---------------

async_job
^^^^^^^^^
.. autodecorator:: regta.async_job

thread_job
^^^^^^^^^^
.. autodecorator:: regta.thread_job

process_job
^^^^^^^^^^^
.. autodecorator:: regta.process_job

AsyncJob
^^^^^^^^
.. autoclass:: regta.AsyncJob
   :members:
   :show-inheritance:

ThreadJob
^^^^^^^^^
.. autoclass:: regta.ThreadJob
   :members:
   :show-inheritance:

ProcessJob
^^^^^^^^^^
.. autoclass:: regta.ProcessJob
   :members:
   :show-inheritance:

run
^^^
.. autofunction:: regta.run

Scheduler
^^^^^^^^^
.. autoclass:: regta.Scheduler
   :members:
   :show-inheritance:

AbstractPeriod
^^^^^^^^^^^^^^
.. autoclass:: regta.AbstractPeriod

Period
^^^^^^
.. autoclass:: regta.Period

PeriodAggregation
^^^^^^^^^^^^^^^^^
.. autoclass:: regta.PeriodAggregation

Weekdays
^^^^^^^^
.. autoclass:: regta.Weekdays


regta.jobs
----------
.. automodule:: regta.jobs
   :exclude-members: AbstractJob, BaseJob, BaseSyncJob, AsyncJob, ThreadJob, ProcessJob, async_job, thread_job, process_job

jobs.AbstractJob
^^^^^^^^^^^^^^^^
.. autoclass:: regta.jobs.AbstractJob
   :members:
   :show-inheritance:

jobs.BaseJob
^^^^^^^^^^^^
.. autoclass:: regta.jobs.BaseJob
   :members:
   :show-inheritance:

jobs.BaseSyncJob
^^^^^^^^^^^^^^^^
.. autoclass:: regta.jobs.BaseSyncJob
   :members:
   :show-inheritance:


regta.schedulers
----------------
.. automodule:: regta.schedulers
   :exclude-members: AbstractScheduler, SyncBlocking, SyncScheduler, AsyncScheduler, Scheduler

schedulers.AbstractScheduler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: regta.schedulers.AbstractScheduler
   :members:
   :show-inheritance:

schedulers.SyncBlocking
^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: regta.schedulers.SyncBlocking
   :members:
   :show-inheritance:

schedulers.SyncScheduler
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: regta.schedulers.SyncScheduler
   :members:
   :show-inheritance:

schedulers.AsyncScheduler
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: regta.schedulers.AsyncScheduler
   :members:
   :show-inheritance:


regta.exceptions
----------------

.. automodule:: regta.exceptions
   :members:
   :show-inheritance:

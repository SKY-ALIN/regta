.. _quick-start:

Quick Start
===========

.. toctree::
   :hidden:

   self
   intervals
   make_jobs
   oop_style
   in_code_start
   schedulers
   logging
   docker

Installation
------------
Install using :code:`pip install regta` or :code:`poetry add regta`.

If you use python < 3.9, then also install backports: :code:`pip install "backports.zoneinfo[tzdata]"`.

You can check if Regta was installed correctly with the following command :code:`regta --help`.

Basic Async Job
---------------
To write async job use :code:`@regta.async_job()` decorator:

.. code-block:: python
    :caption: jobs/my_jobs.py

    from datetime import timedelta
    from regta import async_job, Period


    @async_job(Period().every(10).seconds)
    async def my_period_based_job():
        return "1. Hello world! This is just a log message."


    @async_job(timedelta(seconds=10))
    async def my_timedelta_based_job():
        return "2. You may use `timedelta` or `Period` as interval."


    @async_job(Period().on.sunday.at("18:35").by("Asia/Almaty"))
    async def my_sunday_job():
        return "3. `Period` is recommended for highly responsible jobs because it does not accumulate shift."

These jobs is absolutely unuseful, but it will let us check out how jobs work.

.. note::
   The function can return a string optionally, all function's output will be logged.

Start Job
---------
To start jobs use :code:`regta run` command::

    $ regta run
    > [3] jobs were found.
    > 2023-01-08 18:31:00,005 [jobs.my_jobs:my_period_based_job] [INFO] - 1. Hello world! This is just a log message.
    > 2023-01-08 18:31:05,622 [jobs.my_jobs:my_timedelta_based_job] [INFO] - 2. You may use `timedelta` or `Period` as interval.
    .  .  .
    > 2023-01-08 18:34:50,002 [jobs.my_jobs:my_period_based_job] [INFO] - 1. Hello world! This is just a log message.
    > 2023-01-08 18:34:55,689 [jobs.my_jobs:my_timedelta_based_job] [INFO] - 2. You may use `timedelta` or `Period` as interval.
    > 2023-01-08 18:35:00,001 [jobs.my_jobs:my_sunday_job] [INFO] - 3. `Period` is recommended for highly responsible jobs because it does not accumulate shift.
    .  .  .

.. hint::
   Add flag ``-V`` for verbose output.

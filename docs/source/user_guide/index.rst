.. _quick-start:

Quick Start
===========

.. toctree::
   :hidden:

   self
   make_jobs
   oop_style
   in_code_start
   schedulers
   logging
   docker

Installation
------------
Install using :code:`pip install regta` or :code:`poetry add regta`.
You can check if **regta** was installed correctly with the following command :code:`regta --help`.

Basic Async Job
---------------
To write async job use :code:`@regta.async_job()` decorator:

.. code-block:: python
    :caption: my_job.py

    from datetime import timedelta
    import regta

    @regta.async_job(interval=timedelta(seconds=5))
    async def my_basic_job():
        return "Hello world! This is just a log message."

This job is absolutely unuseful, but it will let us check out how jobs work.

.. note::
   The function can return a string optionally, all function's output will be logged.

Start Job
---------
To start jobs use :code:`regta run` command::

   [1] jobs were found.
   2022-03-30 02:47:18,020 [jobs.my_job:my_basic_job] [INFO] - Hello world! This is just a log message.
   2022-03-30 02:47:23,024 [jobs.my_job:my_basic_job] [INFO] - Hello world! This is just a log message.
   2022-03-30 02:47:28,026 [jobs.my_job:my_basic_job] [INFO] - Hello world! This is just a log message.

.. hint::
   Add flag ``-V`` for verbose output.

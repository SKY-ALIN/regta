Alternatives
============

This page describes popular scheduling alternatives
and provides a comparison.

|cron|_
-------

Cron is the most popular general-purpose scheduler in the world.
This scheduler is universal and lets start jobs as a shell command.
Take note that Cron starts a separate process for every job and
this may take a lot of system resources.
With Cron you also can't use asynchronous programming.
So, Cron might be the best scheduling variant for internal automation
when you have a need to write jobs in different programming languages.

.. _cron: https://en.wikipedia.org/wiki/Cron
.. |cron| replace:: Cron

|schedule|_
------------

``schedule`` is the most popular python scheduling package.
Note, that according to its documentation it doesn't have:

    * Job persistence (remember schedule between restarts)
    * Exact timing (sub-second precision execution)
    * Concurrent execution (multiple threads)
    * Localization (time zones, workdays or holidays)

So, I'd never recommend you use it in real-world systems.
Possible only for a university project or for a pet project.

.. _schedule: https://schedule.readthedocs.io/en/stable/
.. |schedule| replace:: Schedule

|celery|_
---------

Celery is the most popular package for background tasks.
The main goal of this is to organize distributed background tasks,
but it also has an opportunity to start a scheduler that will pass
jobs to the queue, and workers will execute it distributedly.
So, Celery scheduling might be heavy, but the best solution for
external automation with a lot of jobs.
Especially if you already have a Celery cluster.

Read more about `Periodic Tasks in Celery <celery_periodic_tasks_>`_.


.. _celery_periodic_tasks: https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
.. _celery: https://docs.celeryq.dev/en/stable/
.. |celery| replace:: Celery


|apscheduler|_
--------------

APScheduler is a powerful tool with the same benefits as Regta.
The difference is only that Regta uses `moment-independent approach <moment_independence_>`_ to get
restart tolerance ability, but APScheduler uses an external database to cache executing time.
This is the reason why APScheduler might be more complex to configure because you have to manage a database.

.. _moment_independence: https://github.com/SKY-ALIN/regta-period
.. _apscheduler: https://apscheduler.readthedocs.io/
.. |apscheduler| replace:: APScheduler


Conclusion
----------

Finally, you may compare them by the following table:

.. role:: plus
.. role:: minus

.. list-table::
   :align: center
   :header-rows: 1

   * -
     - Regta
     - |cron|_
     - |schedule|_
     - |celery|_
     - |apscheduler|_
   * - Concurrent execution
     - :plus:`+`
     - :plus:`+`
     - :minus:`-`
     - :plus:`+`
     - :plus:`+`
   * - Async support
     - :plus:`+`
     - :minus:`-`
     - :minus:`-`
     - :minus:`-`
     - :plus:`+`
   * - Restart tolerance
     - :plus:`+`
     - :minus:`-`
     - :minus:`-`
     - :minus:`-`
     - :plus:`+`
   * - Exact timing
     - :plus:`+`
     - :plus:`+`
     - :minus:`-`
     - :plus:`+`
     - :plus:`+`
   * - Localization
     - :plus:`+`
     - :minus:`-`
     - :minus:`-`
     - :plus:`+`
     - :plus:`+`
   * - Horizontal scaling
     - :minus:`-`
     - :minus:`-`
     - :minus:`-`
     - :plus:`+`
     - :minus:`-`
   * - Configuration complexity
     - :plus:`Low`
     - :plus:`Low`
     - :plus:`Low`
     - :minus:`High`
     - :minus:`High`

So, if your goal is **internal automation with python** only e.g. sending regular Slack notifications,
making backups, sending internal emails and so on, **Regta might be the best variant** for you.

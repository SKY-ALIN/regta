=============
CLI Reference
=============

regta
-----

.. code-block:: none

    Usage: regta [OPTIONS] COMMAND [ARGS]...

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      execute  Execute a single job once and immediately.
      list     Show the list of found jobs.
      new      Create a new job by template.
      run      Start all jobs.

regta new
---------

.. code-block:: none

    Usage: regta new [OPTIONS] NAME

      Create a new job by template.

    Options:
      -T, --type [async|thread|process]
                                      Job type. Defines how the job will use
                                      system resources.  [default: thread]
      -S, --style [oop|decorator]     Job code style.  [default: decorator]
      -P, --path PATH                 Path to directory with jobs.  [default:
                                      jobs]
      --help                          Show this message and exit.

regta list
----------

.. code-block:: none

    Usage: regta list [OPTIONS]

      Show the list of found jobs.

    Options:
      -P, --path PATH  Path to directory with jobs.  [default: (current
                       directory)]
      --no-ansi        Disable ANSI colors.
      --help           Show this message and exit.

regta run
---------

.. code-block:: none

    Usage: regta run [OPTIONS]

      Start all jobs.

    Options:
      -P, --path PATH    Path to directory with jobs.  [default: (current
                         directory)]
      -L, --logger TEXT  Path to logger factory in the following format:
                         <module>:<logger_factory>. Example:
                         `src.logger:make_jobs_logger`.
      -V, --verbose      Set DEBUG level to logger.
      --no-ansi          Disable ANSI colors.
      --help             Show this message and exit.

regta execute
-------------

.. code-block:: none

    Usage: regta execute [OPTIONS] JOB_URI

      Execute a single job once and immediately.

      JOB_URI - path to the job in following format: <module>:<job>. Example:
      `jobs.database_jobs:make_backup`.

    Options:
      -L, --logger TEXT  Path to logger factory in the following format:
                         <module>:<logger_factory>. Example:
                         `src.logger:make_jobs_logger`.
      -V, --verbose      Set DEBUG level to logger.
      --no-ansi          Disable ANSI colors.
      --help             Show this message and exit.

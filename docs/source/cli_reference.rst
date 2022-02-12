=============
CLI Reference
=============

regta
-----

.. code-block:: bash

    Usage: regta [OPTIONS] COMMAND [ARGS]...

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      list  Shows the list of found jobs.
      new   Creates new job by template.
      run   Starts all jobs.

regta new
---------

.. code-block:: bash

    Usage: regta new [OPTIONS] NAME

      Creates new job by template.

    Options:
      -T, --type [async|thread|process]
                                      Job type. Defines how the job will use
                                      system resources.  [default: thread]
      -S, --style [oop|decorator]     Job code style.  [default: decorator]
      -P, --path PATH                 Path to which the job file will be created.
                                      [default: jobs]
      --help                          Show this message and exit.

regta list
----------

.. code-block:: bash

    Usage: regta list [OPTIONS]

      Shows the list of found jobs.

    Options:
      -P, --path PATH  Path to directory with jobs.  [default: (current
                       directory)]
      --help           Show this message and exit.

regta run
---------

.. code-block:: bash

    Usage: regta run [OPTIONS]

      Starts all jobs.

    Options:
      -P, --path PATH    Path to directory with jobs.  [default: (current
                         directory)]
      -l, --list TEXT    Path to python file with list of jobs descriptions.
                         Format: <module>:<list>, example: package.main:JOBS
      -L, --logger TEXT  Path to python file with logger factory. Format:
                         <module>:<logger_factory>, example:
                         package.logger:make_jobs_logger
      -V, --verbose      A very detailed summary of what's going on.
      --help             Show this message and exit.

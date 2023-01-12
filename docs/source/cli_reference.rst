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
      list  Shows the list of found jobs.
      new   Creates new job by template.
      run   Starts all jobs.

regta new
---------

.. code-block:: none

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

.. code-block:: none

    Usage: regta list [OPTIONS]

      Shows the list of found jobs.

    Options:
      -P, --path PATH  Path to directory with jobs.  [default: (current
                       directory)]
      --no-ansi        Disable ANSI colors.
      --help           Show this message and exit.

regta run
---------

.. code-block:: none

    Usage: regta run [OPTIONS]

      Starts all jobs.

    Options:
      -P, --path PATH    Path to directory with jobs.  [default: (current
                         directory)]
      -L, --logger TEXT  Path to python file with logger factory. Format:
                         <module>:<logger_factory>, example:
                         package.logger:make_jobs_logger
      -V, --verbose      A very detailed summary of what's going on.
      --no-ansi          Disable ANSI colors.
      --help             Show this message and exit.

Logging
=======
Regta provide opportunity to log output of every job. You can specify your
own logger or if you don't, regta will use its logger with standard output
with ansi highlight. To log some job's result just use ``return`` statement.

Logger Factory
--------------
You can't specify logger as a object because of object loader and logging
module specific, but can specify a factory function which will return a
object. See a example of such factory:

.. code-block:: python
   :caption: logger.py

    import logging


    def logger_factory():
        level = logging.DEBUG

        formatter = logging.Formatter('%(asctime)s [%(levelname)s]: - %(message)s')

        handler = logging.FileHandler('output.log')
        handler.setLevel(level)
        handler.setFormatter(formatter)

        logger = logging.getLogger('__main__')
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

Pass Logger
-----------
To pass logger into run command use ``-L/--logger`` option in this format:
``<module>:<logger_factory>``.

.. code-block:: shell

    regta run --logger logger:logger_factory

To pass logger into run function use ``logger`` argument:

.. code-block:: python

   import regta

   from logger import logger_factory

   jobs_list = []  # Stub for example

   regta.run(jobs=jobs_list, logger=logger_factory())

.. note::
   If you use in-code start, you don't have to use logger factory, you can
   specify logger as a object.

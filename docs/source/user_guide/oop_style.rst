OOP Styled Jobs
===============
Every decorator from the last page create one of next classes from your
function, but you can create these class yourself. The examples below are as
simple as possible without any specific implementation, just the logging.
See previous page for examples with concrete implementations.

Async Job
---------
Use :class:`regta.AsyncJob` to build job with this type.

.. code-block:: python

    from datetime import timedelta

    from regta import AsyncJob


    class MyAsyncJob(AsyncJob):
        interval = timedelta(days=7)

        async def execute(self):
            return f"Hello from {self.__class__.__name__}!"


Thread Job
----------
Use :class:`regta.ThreadJob` to build job with this type.

.. code-block:: python

    from datetime import timedelta

    from regta import ThreadJob


    class MyThreadBasedJob(ThreadJob):
        interval = timedelta(hours=1)

        def execute(self):
            return f"Hello from {self.__class__.__name__}!"


Process Job
-----------
Use :class:`regta.ProcessJob` to build job with this type.

.. code-block:: python

    from datetime import timedelta

    from regta import ProcessJob


    class MyProcessBasedJob(ThreadJob):
        interval = timedelta(hours=24)

        def execute(self):
            return f"Hello from {self.__class__.__name__}!"


Code style is only your choice. Just if you have a lot of similar jobs, OOP
style may be more useful.

    The object-oriented model makes it easy to build up programs by
    accretion. What this often means, in practice, is that it provides
    a structured way to write spaghetti code.

    — Paul Graham

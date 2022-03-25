Make Jobs
=========
.. _jobs-types:

Regta provides different jobs types to build different tasks:

To build fast tasks with IO operations e.g. internet requests, database query
or work with files use :ref:`async-job`.

If for some reason you can't use
asynchronous programming, but you are still faced with the task of building
an lightweight job, use :ref:`thread-job`.

To build heavy jobs with a lot of computing e.g. ML or data analytics use
:ref:`process-job`.

All job's output will be logged. If logger factory are not specified,
standard output will be used.

.. seealso::
   What is the logger factory and how to add logging into your project
   :ref:`here <Logging>`.


.. _async-job:

Async Job
---------
Use :class:`regta.async_job` to build job with this type. See example of how to
send regular notification to Slack channel below:

.. code-block:: python

    from aiohttp import ClientSession
    from datetime import datetime, timedelta

    import regta


    class Slack:
        URL: str  # secret url from env

        def __init__(self, channel: str):
            self.channel = channel

        async def send_message(self, message: str):
            async with ClientSession(headers={"Content-type": "application/json"}) as session:
                await session.post(self.URL, json={"text": message, "channel": self.channel})


    @regta.async_job(interval=timedelta(days=7))
    async def weekly_report():
        data = "Some report data..."
        await Slack("my-channel").send_message(data)

        return f"Weekly report was sent at {datetime.utcnow()}."


.. _thread-job:

Thread-Based Job
----------------
Use :class:`regta.thread_job` to build job with this type. See example of how to
mark users as inactive for synchronous version of sqlalchemy:

.. code-block:: python

    from datetime import datetime, timedelta

    import regta

    from db import Session
    from models import User


    @regta.thread_job(interval=timedelta(hours=1))
    def mark_users_as_inactive():
        with Session() as session:
            marked_users_ids = session.execute(
                User
                .update()
                .where(User.active=True, User.last_online < datetime.utcnow() - timedelta(days=365))
                .values(active=False)
                .returning(User.id)
            )

        return f"{len(marked_users_ids)} users was marked as inactive."


.. _process-job:

Process-Based Job
-----------------
Use :class:`regta.process_job` to build job with this type. See example of how to
predict weather by temperature (this is not good example of ML task, but is
ok to demonstrate how to use process-based job) using prepared ML model on
send result into Telegram channel:

.. code-block:: python

    from datetime import datetime, timedelta
    from typing import List

    import regta
    import telebot  # module for Telegram

    from ml_models import my_model  # Stub model for this example


    def get_last_temperature_for_a_week() -> List[float]:
        """This is just a stub function for demonstration."""


    class TelegramChannel:
        CHANNEL_ID: str
        TOKEN: str

        def __init__(self):
            self.bot = telebot.TeleBot(self.TOKEN)

        def post(text: str):
            self.bot.send_message(self.CHANNEL_ID, text)


    @regta.process_job(interval=timedelta(hours=24))
    def send_temperature_prediction():
        prediction = my_model.predict(get_last_temperature_for_a_week())
        result = float(prediction[0])

        msg = f"Tomorrow at this time will be {result}С°"
        TelegramChanel().post(msg)
        return msg


Jobs As A List (Reusing User's Code Base)
-----------------------------------------
To provide already writen functions to regta write a list of dicts where
every dict will have this structure:

.. code-block:: python

    from datetime import timedelta
    from typing import Awaitable, Callable, TypedDict, Iterable, Optional


    class JobDictHint(TypedDict):
        async: Optional[Callable[..., Awaitable[Optional[str]]]]
        thread: Optional[Callable[..., Optional[str]]]
        process: Optional[Callable[..., Optional[str]]]

        interval: dict
        args: Optional[Iterable] = []
        kwargs: Optional[dict] = {}

.. important::
   Only one of async/thread/process keys must be specified. Which one
   means job's type.

See example:

.. code-block:: python

    # jobs/my_python_file.py

    def some_your_function(x1: int, x2: int, factor: float = 1):
        return x1 / x2 * factor

    jobs_list = [
        {
            "thread": some_your_function,
            "interval": {  # will be converted into datetime.interval object
                "minutes": 30,
                "hours": 1,
            },
            "args": [30, 100],  # x1 and x2 as positional args
            "kwargs": {"factor": 0.8}  # factor as key-value arg
        },
        # -- Examples of functions from examples above -- #
        {
            "async": weekly_report,
            "interval": {
                "days": 7,
            },
        },
        {
            "thread": mark_users_as_inactive,
            "interval": {
                "hours": 1,
            },
        },
        {
            "process": send_temperature_prediction,
            "interval": {
                "hours": 24,
            },
        },
    ]

.. note::
   In example of functions list keep in mind ``weekly_report``,
   ``mark_users_as_inactive`` and ``send_temperature_prediction`` must be
   writen without decorators :class:`regta.async_job`,
   :class:`regta.thread_job` and :class:`regta.process_job`.

To pass this list into ``regta run`` command use ``-l``/``--list`` option
(format: ``<module>:<list>``): ``regta run --list jobs.my_python_file:jobs_list``.

.. seealso::
    Check :ref:`regta run` to see more about this command and its options.

Make Jobs
=========
.. _jobs-types:

Regta provides various job types to solve various tasks:

To build fast jobs with IO operations e.g. internet requests, database query
or work with files use :ref:`async-job`.

If for some reason you can't use asynchronous programming, but you are still
faced with a task of building a lightweight job, use :ref:`thread-job`.

To build heavy jobs with a lot of computing e.g. ML or data analytics use
:ref:`process-job`.

All job output will be logged. If logger factory is not specified,
standard output will be used.

.. seealso::
   What is the logger factory and how to add logging into your project
   :ref:`here <Logging>`.


.. _async-job:

Async Job
---------
Use :class:`regta.async_job` to build jobs with this type. See an example of
how to send regular notifications to a Slack channel below:

.. code-block:: python

    from aiohttp import ClientSession
    from datetime import datetime, timedelta

    import regta


    class Slack:
        url: str  # secret URL from env

        def __init__(self, channel: str):
            self.channel = channel

        async def send_message(self, message: str):
            async with ClientSession(headers={"Content-type": "application/json"}) as session:
                await session.post(self.url, json={"text": message, "channel": self.channel})


    @regta.async_job(timedelta(days=7))
    async def weekly_report():
        data = "Some report data..."
        await Slack("my-channel").send_message(data)

        return f"Weekly report was sent at {datetime.utcnow()}."


.. _thread-job:

Thread-Based Job
----------------
Use :class:`regta.thread_job` to build jobs with this type. See an example of
how to mark users as inactive for the synchronous version of sqlalchemy:

.. code-block:: python

    from datetime import datetime, timedelta

    import regta

    from db import Session
    from models import User


    @regta.thread_job(timedelta(hours=1))
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
Use :class:`regta.process_job` to build jobs with this type. See an example of
how to predict the weather by temperature (this is not a good example of a ML
task, but is ok to demonstrate how to use a process-based job) using prepared
ML model and send the result on a Telegram channel:

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


    @regta.process_job(timedelta(hours=24))
    def send_temperature_prediction():
        prediction = my_model.predict(get_last_temperature_for_a_week())
        result = float(prediction[0])

        msg = f"Tomorrow at this time will be {result}С°"
        TelegramChanel().post(msg)
        return msg

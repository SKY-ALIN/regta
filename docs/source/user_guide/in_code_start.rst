CLI vs. In-Code Start
=====================
There are different ways to start your jobs. Let's review and compare them.

CLI Starting
------------
We recommend using this way because it's the easier way and more stable way.
This approach means using the CLI tool to start.
Just type ``regta run`` to start.
It will load your jobs from all project files and pass them to
:class:`regta.run` function.
See :ref:`regta run` section for more information about this command.

Run Function
------------
If you have some specific pre-init script, you can use :class:`regta.run`
directly.
This function will create a :class:`regta.Scheduler`, pass your jobs there and
start it.
See :ref:`API Reference <run>` for more.

Using Scheduler
---------------
If you're going to use regta parallel with another framework, you can
switch off thread blocking.
For this use one of schedulers directly and pass ``block=True`` into
:attr:`regta.Scheduler.run`.
See main :class:`regta.Scheduler` and others
:ref:`schedulers <regta.schedulers>` for more information.

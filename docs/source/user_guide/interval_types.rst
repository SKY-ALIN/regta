Interval Types
==============

:class:`datetime.timedelta`
---------------------------

Timedelta is a standard class to define time intervals. It's may be used as an interval for Regta too, but be careful because of the following reasons:

* When you use a timedelta object you will have a shift accumulation because of execution time.
  For example, if a job interval is 5 minutes, but the execution time of the job is 1 min,
  then the final interval between every execution will be 6 minutes.
  So, it means you will have 240 times of execution per day instead of 288.

* You will get a shift after every scheduler restart because every time Regta starts clocking from the beginning.
  So, for example, if you restart your server because of CI/CD too often, the shift may be critical.


|period-class|_
---------------

``Period`` is an interval class specially designed for Regta.
Period objects are more flexible because they let specify an exact time of execution and a lot of additional useful options.
Also, they are devoid of the disadvantages of ``timedelta``.

It has been placed in a separate package |regta-period-github|_, but it is fully integrated into this package.

.. code-block:: python

   from regta import Period

   # Every 3 days at 5 pm by Moscow time
   p1 = Period().every(3).days.at("17:00").by("Europe/Moscow")

   # At 6 pm on weekdays (Monday-Friday) and at 9 pm on weekends (Saturday-Sunday)
   p2 = Period().on.weekdays.at("18:00") | Period().on.weekends.at("21:00")

   # The same, but more human-readable:)
   p2 = Period().on.weekdays.at("18:00").OR.on.weekends.at("21:00")

Since it is a separate package, the documentation is hosted on a separate domain: |regta-period-docs|_.
There you can find more examples of use and a detailed description of how it works.


.. _regta-period-github: https://github.com/SKY-ALIN/regta-period
.. |regta-period-github| replace:: ``regta-period``
.. _regta-period-docs: https://regta-period.alinsky.tech/
.. |regta-period-docs| replace:: **regta-period.alinsky.tech**
.. _period-class: https://regta-period.alinsky.tech/api_reference#period
.. |period-class| replace:: ``regta_period.Period``

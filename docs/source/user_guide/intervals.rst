Intervals
=========

:class:`datetime.timedelta`
---------------------------

Timedelta is a standard class to define time intervals. It's may be used as a interval for Regta too, but be careful because of the following reasons:

* When you use a timedelta object you will have a shift accumulation because of execution time.
  For example, if a job interval is 5 minutes, but the execution time of the job is 1 min,
  then the final interval between every execution will be 6 minutes.
  So, it means you will have 240 times of execution per day instead of 288.

* You will get a shift after every scheduler restart because every time Regta starts clocking from the beginning.
  So, for example, if you restart your server because of CI/CD too often, the shift may be critical.


|period-class|_
---------------

Period is a interval class especially designed for Regta.
Period objects are more flexible because they let specify an exact time of execution and has a lot of additional useful options.
Also, they are devoid of the disadvantages of timedelta.

It has been placed in a separate package (`regta-period <regta-period-github_>`_), but it is fully integrated into this package.

Since it is a separate package, the documentation is hosted on a separate domain: `regta-period.alinsky.tech <regta-period_>`_


.. _regta-period: https://regta-period.alinsky.tech/
.. _period-class: https://regta-period.alinsky.tech/api_reference#period
.. |period-class| replace:: ``regta_period.Period``
.. _regta-period-github: https://github.com/SKY-ALIN/regta-period

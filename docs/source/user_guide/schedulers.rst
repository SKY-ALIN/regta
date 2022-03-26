Schedulers
==========
Scheduler starts and stops jobs. There are different schedulers for different
jobs' types. Every Scheduler provide common interface, see
:class:`regta.schedulers.AbstractScheduler`.

Sync Scheduler
--------------
:class:`regta.schedulers.SyncScheduler` is used for all sync jobs:
:class:`regta.ThreadJob` and :class:`regta.ProcessJob`.

Async Scheduler
---------------
:class:`regta.schedulers.AsyncScheduler` is used for :class:`regta.AsyncJob`
only.

Main Scheduler
--------------
:class:`regta.Scheduler` internally declares both schedulers and manages
them. Honestly, you can forget sync and async schedulers ever existed and use
only it because it uses them inside. This is recommended way.

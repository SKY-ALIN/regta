## 0.3.0 (27.01.2023)
* Add `regta-period` package support
* Remove support for jobs loading as `--list` param
* Add `--no-ansi` flag to `regta run` and `regta list` commands
* Add `regta execute` command
* Set DEBUG level to logger if verbose flag is set

## 0.2.0 (31.3.2022)
* Add logging
* Add decorator job style (`@regta.async_job`, `@regta.thread_job`, `@regta.process_job`)
* Production ready execution
* Add docs

## 0.1.0-alpha.0 (27.11.2021)
* CLI interface to create, list and run jobs.
* Jobs' classes `AsyncJob`, `ThreadJob` and `ProcessJob`.
* Schedulers `AsyncScheduler`, `SyncScheduler` and `Scheduler` (include `AsyncScheduler` and `SyncScheduler` schedulers).

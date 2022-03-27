## regta
**Lightweight framework to create and execute periodic async and sync jobs on 
different processes, threads and event loop.**

[![pypi](https://img.shields.io/pypi/v/regta.svg)](https://pypi.python.org/pypi/regta)
[![versions](https://img.shields.io/pypi/pyversions/regta.svg)](https://github.com/SKY-ALIN/regta)
[![license](https://img.shields.io/github/license/SKY-ALIN/regta.svg)](https://github.com/SKY-ALIN/regta/blob/master/LICENSE)


### Features

Different Jobs
: Create async, thread-based or process-based jobs depending on your goals.

Support different code styles
: Create OOP styled or functional styled jobs. Regta also provide interface to reuse
  user's already written code.

CLI interface to work with jobs
: Regta provide CLI tool to list and start available written jobs.

Logging
: Redefine standard and define your own logging way.

---

### Installation
Install using `pip install regta` or `poetry add regta`. 
You can check if **regta** was installed correctly with the following 
command `regta --help`.

### Example
To write async job use `@regta.async_job()` decorator
```python
# jobs/some_async_job.py

from datetime import timedelta
import regta

@regta.async_job(interval=timedelta(seconds=5))
async def my_basic_job():
    return "Hello world! This is just a log message."
```

### Start up
To start jobs use `regta run` command:
```shell
$ regta run
> [1] jobs were found.
> jobs.some_async_job:my_basic_job - Hello world! This is just a log message.
.  .  .
```

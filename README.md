# regta

**Production-ready scheduler with async, multithreading and multiprocessing support for Python.**

[![versions](https://img.shields.io/pypi/pyversions/regta.svg)](https://github.com/SKY-ALIN/regta)
![Code Quality](https://github.com/SKY-ALIN/regta/actions/workflows/code-quality.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/regta.svg)](https://pypi.org/project/regta/)
[![license](https://img.shields.io/github/license/SKY-ALIN/regta.svg)](https://github.com/SKY-ALIN/regta/blob/main/LICENSE)

### Core Features

- **[Various job types](https://regta.alinsky.tech/user_guide/make_jobs)** - Create async, thread-based,
  or process-based jobs depending on your goals.


- **[Support different code styles](https://regta.alinsky.tech/user_guide/oop_style)** - Design OOP styled
  or functional styled jobs. Regta also provides an interface to reuse user's already written code.


- **[CLI interface to work with jobs](https://regta.alinsky.tech/cli_reference)** - Regta provides a CLI tool
  to list and start available written jobs.


- **[Logging](https://regta.alinsky.tech/user_guide/logging)** - Redefine standard and define your own logging.

---

### Installation
Install using `pip install regta` or `poetry add regta`. 
You can check if **regta** was installed correctly with the following 
command `regta --help`.

### Example
To write async job just use `@regta.async_job()` decorator.
```python
# jobs/my_job.py

from datetime import timedelta
import regta

@regta.async_job(timedelta(seconds=5))
async def my_basic_job():
    return "Hello world! This is just a log message."
```
See more about various job types 
[here](https://regta.alinsky.tech/user_guide/make_jobs).

### Start Up
To start jobs use `regta run` command:
```shell
$ regta run
> [1] jobs were found.
> 2022-03-30 02:47:18,020 [jobs.my_job:my_basic_job] [INFO] - Hello world! This is just a log message.
> 2022-03-30 02:47:23,024 [jobs.my_job:my_basic_job] [INFO] - Hello world! This is just a log message.
> 2022-03-30 02:47:28,026 [jobs.my_job:my_basic_job] [INFO] - Hello world! This is just a log message.
.  .  .
```
See CLI reference [here](https://regta.alinsky.tech/cli_reference).

---

Full documentation and reference are available on 
[regta.alinsky.tech](https://regta.alinsky.tech)

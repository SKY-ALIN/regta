# regta

**Production-ready scheduler with async, multithreading and multiprocessing support for Python.**

[![versions](https://img.shields.io/pypi/pyversions/regta.svg)](https://github.com/SKY-ALIN/regta)
![Code Quality](https://github.com/SKY-ALIN/regta/actions/workflows/code-quality.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/regta.svg)](https://pypi.org/project/regta/)
[![license](https://img.shields.io/github/license/SKY-ALIN/regta.svg)](https://github.com/SKY-ALIN/regta/blob/main/LICENSE)

### Core Features

- **[Various Job Types](https://regta.alinsky.tech/user_guide/make_jobs)** - Create async, thread-based,
  or process-based jobs depending on your goals.


- **[Flexible Intervals](https://regta.alinsky.tech/user_guide/interval_types)** - Use standard `timedelta`
  object or specially designed `Period` for highly responsible jobs.


- **[Multi-Paradigm](https://regta.alinsky.tech/user_guide/oop_style)** - Design OOP styled
  or functional styled jobs.


- **[CLI Interface](https://regta.alinsky.tech/cli_reference)** - Regta provides a CLI tool
  to start, list and create jobs by template.


- **[Professional Logging](https://regta.alinsky.tech/user_guide/logging)** - Redefine standard logger
  and define your own. ANSI coloring is supported.

---

### Installation
Install using `pip install regta` or `poetry add regta`.

If you use python < 3.9, then also install backports: `pip install "backports.zoneinfo[tzdata]"`.

You can check if Regta was installed correctly with the following command `regta --version`.

### Example

To write async job just use `@regta.async_job()` decorator.

```python
# jobs/my_jobs.py

from datetime import timedelta
from regta import async_job, Period


@async_job(Period().every(10).seconds)
async def my_period_based_job():
    return "1. Hello world! This is just a log message."


@async_job(timedelta(seconds=10))
async def my_timedelta_based_job():
    return "2. You may use `timedelta` or `Period` as interval."


@async_job(Period().on.sunday.at("18:35").by("Asia/Almaty"))
async def my_sunday_job():
    return "3. `Period` is recommended for highly responsible jobs because it does not accumulate shift."
```

Read more about various job types 
[here](https://regta.alinsky.tech/user_guide/make_jobs).

### Start Up

To start jobs use `regta run` command:

```shell
$ regta run
> [3] jobs were found.
> 2023-01-08 18:31:00,005 [jobs.my_jobs:my_period_based_job] [INFO] - 1. Hello world! This is just a log message.
> 2023-01-08 18:31:05,622 [jobs.my_jobs:my_timedelta_based_job] [INFO] - 2. You may use `timedelta` or `Period` as interval.
.  .  .
> 2023-01-08 18:34:50,002 [jobs.my_jobs:my_period_based_job] [INFO] - 1. Hello world! This is just a log message.
> 2023-01-08 18:34:55,689 [jobs.my_jobs:my_timedelta_based_job] [INFO] - 2. You may use `timedelta` or `Period` as interval.
> 2023-01-08 18:35:00,001 [jobs.my_jobs:my_sunday_job] [INFO] - 3. `Period` is recommended for highly responsible jobs because it does not accumulate shift.
.  .  .
```

Read CLI reference [here](https://regta.alinsky.tech/cli_reference).

---

Full documentation and reference are available on 
[regta.alinsky.tech](https://regta.alinsky.tech)

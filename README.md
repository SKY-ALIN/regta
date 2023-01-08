# regta

**Production-ready scheduler with async, multithreading and multiprocessing support for Python.**

[![versions](https://img.shields.io/pypi/pyversions/regta.svg)](https://github.com/SKY-ALIN/regta)
![Code Quality](https://github.com/SKY-ALIN/regta/actions/workflows/code-quality.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/regta.svg)](https://pypi.org/project/regta/)
[![license](https://img.shields.io/github/license/SKY-ALIN/regta.svg)](https://github.com/SKY-ALIN/regta/blob/main/LICENSE)

### Core Features

- **[Various job types](https://regta.alinsky.tech/user_guide/make_jobs)** - Create async, thread-based,
  or process-based jobs depending on your goals.


- **[Flexible Intervals](https://regta.alinsky.tech/user_guide/intervals)** - Use standard `timedelta` object or
  specially designed `Period` for highly responsible jobs.


- **[Multi-paradigm](https://regta.alinsky.tech/user_guide/oop_style)** - Design OOP styled
  or functional styled jobs. Also, Regta provides an interface to reuse already written code with config.


- **[CLI interface](https://regta.alinsky.tech/cli_reference)** - Regta provides a CLI tool
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
# jobs/my_job.py

from regta import async_job, Period

@async_job(Period().every(10).seconds)
async def my_basic_job():
    return "Hello world! This is just a log message."
```
Read more about various job types 
[here](https://regta.alinsky.tech/user_guide/make_jobs).

### Start Up
To start jobs use `regta run` command:
```shell
$ regta run
[1] jobs were found.
> 2023-01-08 16:53:00,001 [temp.test:my_basic_job] [INFO] - Hello world! This is just a log message.
> 2023-01-08 16:53:10,002 [temp.test:my_basic_job] [INFO] - Hello world! This is just a log message.
> 2023-01-08 16:53:20,001 [temp.test:my_basic_job] [INFO] - Hello world! This is just a log message.
.  .  .
```
Read CLI reference [here](https://regta.alinsky.tech/cli_reference).

---

Full documentation and reference are available on 
[regta.alinsky.tech](https://regta.alinsky.tech)

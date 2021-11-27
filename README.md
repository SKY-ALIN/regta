# regta
**Lightweight framework for executing periodic async and sync jobs in python.**

[![pypi](https://img.shields.io/pypi/v/regta.svg)](https://pypi.python.org/pypi/regta)
[![versions](https://img.shields.io/pypi/pyversions/regta.svg)](https://github.com/SKY-ALIN/regta)
[![license](https://img.shields.io/github/license/SKY-ALIN/regta.svg)](https://github.com/SKY-ALIN/regta/blob/master/LICENSE)

## Installation
Install using `pip install regta` or `poetry add regta`. 
You can check if **regta** was installed correctly with the following command `regta --help`.

## Samples

### To automatically create basic job use `regta new` command. 
You can specify the job type `[async|thread|process]` as `--type` param.
You can **always** see other options by using the `--help` flag.
```shell
$ regta new some-async-job --type async
> Async job some_async_job in the decorator code style have been created at jobs/some_async_job.py.
```

The previous command will create about this kind of code in `jobs/some_async_job.py`:
```python
from datetime import timedelta

import regta


@regta.async_job(interval=timedelta(seconds=55))
async def some_async_job():
    """Everything this function returns will be logged. If an exception
    occurs in this function, it will be logged as an error.
    """
    # Put your code here
    return "Hello from some_async_job! This message is displayed every 55 seconds."
```

### To show the jobs list use `regta list` command:
```shell
$ regta list
> [1] jobs were found at ./:
> * jobs.some_async_job:some_async_job
```

### To start all jobs use `regta run` command:
```shell
$ regta run
> [1] jobs were found.
> jobs.some_async_job:some_async_job - Hello from some_async_job! This message is displayed every 55 seconds.
.  .  .
```

If you do not want to use the provided decorators style and OOP (`regta new name --style oop`), 
and you would like to easily reuse functions you have already written, 
you can simply describe them as a list:

[comment]: <> (`jobs/main.py`:)
```python
# jobs/main.py

def your_function(name):
    print(f"Hello, {name}!")

TASKS = [
    {
        "thread": your_function,
        "kwargs": {"name": "User"},
        "interval": {
            "minutes": 5,
        },
    },
]
```
...and pass them to the `regta run` command as `--list` param:
```shell
$ regta run --list jobs.main:TASKS
> [1] jobs were found.
> Hello, User!  # code of job
.  .  .
```
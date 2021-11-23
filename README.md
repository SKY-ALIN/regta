## regta
Lightweight framework for executing periodic async and sync jobs in python.

### Installation
Install using `pip install regta` or `poetry add regta`. 
You can check if **regta** was installed correctly with the following command
`regta --version`, the correct output would be approximately `regta, version 0.1.0`.

### Samples

#### To automatically create basic job use `regta new` command. 
You can specify the job type `[async|thread|process]`.
You can **always** see other options by using the `--help` flag.
```shell
$ regta new some-async-job --type async
> Async job SomeAsyncJob have been created at jobs/some_async_job.py.
```

The previous command will create about this kind of code in `jobs/some_async_job.py`:
```python
from datetime import timedelta

from regta import AsyncJob


class SomeAsyncJob(AsyncJob):
    INTERVAL = timedelta(seconds=3)

    async def execute(self):  # function is called every 3 seconds
        print(
            f"Hello from {self.__class__.__name__}! "
            f"This message is displayed every {self.INTERVAL.seconds} seconds."
        )
```

#### To show the jobs list use `regta list` command:
```shell
$ regta list
> [1] jobs were found at ./:
> * SomeAsyncJob   at jobs.some_async_job
```

#### To start regta and all jobs use `regta run` command:
```shell
$ regta run
> [1] jobs were found.
> Hello from SomeAsyncJob! this message is displayed every 3 seconds.  # code of job
.  .  .
```

If you do not want to use the provided OOP, 
and you would like to easily reuse functions you have already written, 
you can simply describe them as a list and pass them to the `regta run` command as `--list` param:
```shell
$ regta run --list jobs.main:TASKS
> [1] jobs were found.
> Hello, User!  # code of job
.  .  .
```
`jobs/main.py`:
```python
def your_function(name):
    print(f"Hello, {name}!")

TASKS = [
    {
        "callable": your_function,
        "kwargs": {"name": "User"},
        "interval": {
            "minutes": 5,
        },
    },
]
```
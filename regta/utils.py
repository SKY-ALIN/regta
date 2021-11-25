import re
import string
from datetime import timedelta
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from importlib import import_module
import inspect
from typing import List, Type

import click

from .enums import JobTypes
from .jobs import JobHint, jobs_classes
from .scheduler import Scheduler


def _fix_name(s: str) -> str:
    return s.replace(' ', '_').translate(str.maketrans(string.punctuation, '_'*len(string.punctuation)))


def to_snake_case(s: str) -> str:
    s = _fix_name(s)
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower().replace('__', '_')


def to_camel_case(s: str) -> str:
    s = _fix_name(s)
    return ''.join(word.title() for word in s.split('_'))


def add_init_file(path: Path):
    init_path = path / "__init__.py"
    init_path.touch(exist_ok=True)


def show_jobs_info(jobs: list, path: Path = None, verbose: bool = False):
    count = click.style(
        len(jobs),
        fg='green' if len(jobs) > 0 else 'red'
    )
    path_str = (
        f" at {click.style(f'{path}/', fg='green')}"
        if path is not None
        else ""
    )
    end_char = ':' if verbose and len(jobs) > 0 else '.'
    click.echo(f"[{count}] jobs were found{path_str}{end_char}")

    if verbose:
        for job in sorted(jobs, key=lambda j: j.__name__ if inspect.isclass(j) else j.__class__.__name__):
            cls = job if inspect.isclass(job) else job.__class__
            click.echo(f"* {cls.__module__}:{click.style(cls.__name__, fg='blue')}")


def load_jobs(path: Path) -> List[Type[JobHint]]:
    jobs = []
    for file in path.glob('**/*.py'):
        if file.parts[0][0] == '.':  # skip hidden
            continue

        module_name = ".".join(file.with_suffix("").parts)
        spec = spec_from_file_location(module_name, file)
        foo = module_from_spec(spec)
        spec.loader.exec_module(foo)

        jobs.extend(
            cls[1]
            for cls
            in inspect.getmembers(foo, inspect.isclass)
            if issubclass(cls[1], tuple(jobs_classes.values()))
            and cls[0] not in (job_class.__name__ for job_class in jobs_classes.values())
        )
    return jobs


def load_list(uri: str) -> List[dict]:
    module_name, list_name = uri.split(':')
    module = import_module(module_name)
    return getattr(module, list_name)


def make_job_from_dict(job_dict: dict) -> JobHint:
    kwargs = {
        "interval": timedelta(**job_dict['interval']),
        "args": job_dict.get('args', []),
        "kwargs": job_dict.get('kwargs', {}),
    }
    for job_type in JobTypes:
        if job_type.value in job_dict:
            job = jobs_classes[job_type](execute=job_dict[job_type.value], **kwargs)
            break
    else:
        raise ValueError("Unknown dictionary meaning, impossible to create a job")
    return job


def make_jobs_from_list(jobs_list: List[dict]) -> List[JobHint]:
    return [make_job_from_dict(job_dict) for job_dict in jobs_list]


def run_jobs(jobs: List[JobHint] = None, classes: List[Type[JobHint]] = None):
    if not jobs and not classes:
        return

    scheduler = Scheduler()
    for job in jobs:
        scheduler.add_job(job)
    for job_class in classes:
        scheduler.add_job(job_class())
    scheduler.run(block=True)

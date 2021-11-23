"""Lightweight framework for executing periodic async and sync jobs in python.
See details on the homepage at https://github.com/SKY-ALIN/regta/"""

from datetime import timedelta
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from importlib import import_module
import inspect
from typing import List, Union, Type
import random

import click

from . import __version__
from .enums import JobTypes, job_templates
from .utils import add_init_file, to_camel_case, to_snake_case
from .jobs import AsyncJob, ThreadJob, ProcessJob, jobs_classes
from .scheduler import Scheduler

JobHint = Union[AsyncJob, ThreadJob, ProcessJob]
JobClassListHint = List[Union[Type[AsyncJob], Type[ThreadJob], Type[ProcessJob]]]
JobListHint = List[JobHint]


@click.group(help=__doc__)
@click.version_option(__version__)
def main(): pass


def show_jobs_info(jobs, path: Path = None, verbose: bool = False):
    count = click.style(
        len(jobs),
        fg='green' if len(jobs) > 0 else 'red'
    )
    path_str = (
        f" at {click.style(f'{path}/', fg='green')}"
        if path is not None
        else ""
    )
    click.echo(f"[{count}] jobs were found{path_str}{':' if verbose and len(jobs) > 0 else '.'}")
    if verbose:
        for job in jobs:
            cls = job if inspect.isclass(job) else job.__class__
            click.echo(f"* {click.style(cls.__name__, fg='blue')}\t at {cls.__module__}")


def load_jobs(path: Path) -> JobClassListHint:
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


def make_jobs_from_list(jobs_list: List[dict]) -> JobListHint:
    return [make_job_from_dict(job_dict) for job_dict in jobs_list]


def run_jobs(jobs: JobListHint = None, classes: JobClassListHint = None):
    if not jobs and not classes:
        return

    scheduler = Scheduler()
    for job in jobs:
        scheduler.add_job(job)
    for job_class in classes:
        scheduler.add_job(job_class())
    scheduler.run(block=True)


@main.command()
@click.option(
    '--path', '-P', 'path',
    default=Path('.'),
    show_default='current directory',
    type=Path,
    help='Path to directory with jobs.',
)
@click.option(
    '--list', '-L', 'jobs_list',
    help=(
        'Path to python file with list of jobs descriptions. '
        'Format: <module>:<list>, example: package.main:JOBS'
    ),
)
@click.option(
    '--verbose', '-V', 'verbose',
    is_flag=True,
    help="A very detailed summary of what's going on."
)
def run(path: Path, jobs_list: str, verbose: bool):
    """Start all jobs."""

    jobs = []
    classes = []
    if jobs_list:
        jobs = make_jobs_from_list(load_list(jobs_list))
    else:
        classes = load_jobs(path)
    show_jobs_info(jobs+classes, verbose=verbose)
    run_jobs(jobs=jobs, classes=classes)


@main.command()
@click.argument('name', type=str)
@click.option(
    '--type', '-T', 'job_type',
    default=JobTypes.THREAD.value,
    show_default=True,
    type=click.Choice([job_type.value for job_type in JobTypes]),
    help="Specify a job's type.",
)
@click.option(
    '--path', '-P', 'path',
    default=Path('jobs/'),
    show_default=True,
    type=Path,
    help='Path to which the job file will be created.',
)
def new(name: str, job_type: str, path: Path):
    """Create new job by template."""

    if name[-3:].lower() != 'job':
        name += "-job"
    file_name = f"{to_snake_case(name)}.py"
    class_name = to_camel_case(name)

    template = job_templates[JobTypes(job_type)]
    path.mkdir(parents=True, exist_ok=True)
    add_init_file(path)
    with open(path / file_name, 'w') as job_file:
        job_file.write(template.render(class_name=class_name, seconds=random.randint(1, 60)))

    click.echo(
        f"{job_type.capitalize()} job {click.style(class_name, fg='blue')} "
        f"have been created at {click.style(path / file_name, fg='blue')}."
    )


@main.command(name='list')
@click.option(
    '--path', '-P', 'path',
    default=Path('.'),
    show_default='current directory',
    type=Path,
    help='Path to directory with jobs.',
)
def list_command(path: Path):
    """Show the list of found jobs."""

    jobs = load_jobs(path)
    show_jobs_info(jobs, path=path, verbose=True)

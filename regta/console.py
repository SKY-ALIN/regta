"""Lightweight framework for executing periodic async and sync jobs in python.
See details on the homepage at https://github.com/SKY-ALIN/regta/"""

from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import inspect
from typing import List, Union, Type

import click

from . import __version__
from .enums import JobTypes, job_templates
from .utils import add_init_file, to_camel_case, to_snake_case
from .jobs import AsyncJob, ThreadJob, ProcessJob
from .scheduler import SyncScheduler

JobListHint = List[Union[Type[AsyncJob], Type[ThreadJob], Type[ProcessJob]]]


@click.group(help=__doc__)
@click.version_option(__version__)
def main(): pass


def show_jobs_info(jobs: JobListHint, path: Path = None, verbose: bool = False):
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
            click.echo(f"* {click.style(job.__name__, fg='blue')}\t at {job.__module__}")


def load_jobs(path: Path) -> JobListHint:
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
            if issubclass(cls[1], (AsyncJob, ThreadJob, ProcessJob))
            and cls[0] not in (AsyncJob.__name__, ThreadJob.__name__, ProcessJob.__name__)
        )
    return jobs


def start_jobs(jobs: JobListHint):
    if not jobs:
        return

    scheduler = SyncScheduler()
    for job in jobs:
        scheduler.add_job(job())
    scheduler.start(block=True)


@main.command()
@click.option(
    '--path', '-P', 'path',
    default=Path('.'),
    show_default='current directory',
    type=Path,
    help='Path to directory with jobs.',
)
@click.option(
    '--list', '-L', 'jobs_description_list',
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
def run(path: Path, jobs_description_list: str, verbose: bool):
    """Start all jobs."""

    jobs = load_jobs(path)
    show_jobs_info(jobs, verbose=verbose)
    click.secho(f"path={path}, list={jobs_description_list}, verbose={verbose}", fg="green")
    start_jobs(jobs)


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
        job_file.write(template.render(class_name=class_name))

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

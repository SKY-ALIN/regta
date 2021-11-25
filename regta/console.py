"""Lightweight framework for executing periodic async and sync jobs in python.
See details on the homepage at https://github.com/SKY-ALIN/regta/"""

from pathlib import Path

import click

from . import __version__
from .enums import JobTypes
from .templates import generate_job
from .utils import (
    make_jobs_from_list,
    load_list,
    load_jobs,
    run_jobs,
    show_jobs_info,
)


@click.group(help=__doc__)
@click.version_option(__version__)
def main(): pass


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
    click.secho("All tasks are closed correctly.", fg='green')


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

    file_name, class_name = generate_job(name, JobTypes(job_type), path)
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

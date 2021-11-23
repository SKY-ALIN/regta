"""Lightweight framework for executing periodic async and sync jobs in python."""

from pathlib import Path

import click

from . import __version__
from .enums import JobTypes


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
    '--list', '-L', 'jobs_description_list',
    help=(
        'Path to python file with list of jobs descriptions. '
        'Format: <module>:<list>, example: package.main:JOBS'
    ),
)
def run(path: Path, jobs_description_list: str):
    """Start all jobs."""
    click.secho(f"path={path}, list={jobs_description_list}", fg="green")


@main.command()
@click.argument('name', type=str)
@click.option(
    '--type', '-T', 'job_type',
    default=JobTypes.THREAD.value,
    show_default=JobTypes.THREAD.value,
    type=click.Choice([job_type.value for job_type in JobTypes]),
    help="Specify a job's type.",
)
def create(name: str, job_type: str):
    """Create new job by default template."""
    click.secho(f"name={name}, type={job_type}", fg="blue")

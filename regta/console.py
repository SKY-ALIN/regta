"""Lightweight framework for executing periodic async and sync jobs in python.
See details on the homepage at https://github.com/SKY-ALIN/regta/"""

from pathlib import Path

import click

from . import __version__
from .enums import JobTypes, job_templates
from .utils import to_camel_case, to_snake_case


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
@click.option(
    '--verbose', '-V', 'verbose',
    is_flag=True,
    help="A very detailed summary of what's going on."
)
def run(path: Path, jobs_description_list: str, verbose: bool):
    """Start all jobs."""
    click.secho(f"path={path}, list={jobs_description_list}, verbose={verbose}", fg="green")


@main.command()
@click.argument('name', type=str)
@click.option(
    '--type', '-T', 'job_type',
    default=JobTypes.THREAD.value,
    show_default=True,
    type=click.Choice([job_type.value for job_type in JobTypes]),
    help="Specify a job's type.",
)
def create(name: str, job_type: str):
    """Create new job by template."""
    if name[-3:].lower() != 'job':
        name += "-job"
    file_name = f"{to_snake_case(name)}.py"
    class_name = to_camel_case(name)

    template = job_templates[JobTypes(job_type)]
    with open(Path('.') / file_name, 'w') as job_file:
        job_file.write(template.render(class_name=class_name))

    click.echo(
        f"{job_type.capitalize()} job {click.style(class_name, fg='blue')} "
        f"have been created at {click.style(file_name, fg='blue')}."
    )

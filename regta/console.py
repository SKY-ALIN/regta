"""Lightweight framework to create and execute periodic async and sync jobs on
different processes, threads, and event loops.
See details on the homepage at https://github.com/SKY-ALIN/regta/
"""

from typing import Callable, List, Union

from logging import Logger
from pathlib import Path

import click

from . import __version__
from .enums import CodeStyles, JobTypes
from .logging import empty_log_format, JobLoggerAdapter, make_default_logger, prod_log_format
from .templates import generate_decorator_styled_job, generate_oop_styled_job
from .utils import load_jobs, load_object, make_jobs_from_list, run_jobs, show_jobs_info


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
    '--list', '-l', 'jobs_list_uri',
    help=(
        'Path to python file with a list of jobs descriptions. '
        'Format: <module>:<list>, example: package.main:JOBS'
    ),
)
@click.option(
    '--logger', '-L', 'logger_uri',
    help=(
        'Path to python file with logger factory. '
        'Format: <module>:<logger_factory>, example: package.logger:make_jobs_logger'
    ),
)
@click.option(
    '--verbose', '-V', 'verbose',
    is_flag=True,
    help="A very detailed summary of what's going on."
)
def run(path: Path, jobs_list_uri: str, logger_uri: str, verbose: bool):
    """Starts all jobs."""

    use_ansi = True
    prod = True

    jobs = []
    classes = []
    if jobs_list_uri:
        jobs_list: List[dict] = load_object(jobs_list_uri)
        jobs = make_jobs_from_list(jobs_list)
    else:
        classes = load_jobs(path)

    logger_factory: Union[Callable[[], Logger], None] = load_object(logger_uri) if logger_uri else None
    logger: Logger = (
        logger_factory()
        if logger_factory
        else make_default_logger(use_ansi=use_ansi, fmt=(prod_log_format if prod else empty_log_format))
    )
    wrapped_logger = JobLoggerAdapter(
        logger,
        plain_job_name='regta',
        styled_job_name=click.style('regta', fg='magenta'),
        use_ansi=use_ansi,
    )

    show_jobs_info(jobs=jobs, classes=classes, verbose=verbose, logger=wrapped_logger, use_ansi=use_ansi)

    try:
        run_jobs(jobs=jobs, classes=classes, logger=logger)
    except ValueError as e:
        wrapped_logger.info(click.style(str(e), fg='red') if use_ansi else str(e))
    else:
        end_str = "All jobs are closed correctly."
        wrapped_logger.info(click.style(end_str, fg='green') if use_ansi else end_str)


@main.command()
@click.argument('name', type=str)
@click.option(
    '--type', '-T', 'job_type',
    default=JobTypes.THREAD.value,
    show_default=True,
    type=click.Choice([job_type.value for job_type in JobTypes]),
    help="Job type. Defines how the job will use system resources.",
)
@click.option(
    '--style', '-S', 'code_style',
    default=CodeStyles.DECORATOR.value,
    show_default=True,
    type=click.Choice([style.value for style in CodeStyles]),
    help="Job code style.",
)
@click.option(
    '--path', '-P', 'path',
    default=Path('jobs/'),
    show_default=True,
    type=Path,
    help='Path to which the job file will be created.',
)
def new(name: str, job_type: str, code_style: str, path: Path):
    """Creates new job by template."""

    style = CodeStyles(code_style)
    if style is CodeStyles.DECORATOR:
        file_name, class_name = generate_decorator_styled_job(name, JobTypes(job_type), path)
    elif style is CodeStyles.OOP:
        file_name, class_name = generate_oop_styled_job(name, JobTypes(job_type), path)
    else:
        raise ValueError("Incorrect job code style")

    click.echo(
        f"{job_type.capitalize()} job {click.style(class_name, fg='blue')} "
        f"in the {code_style} code style have been created at {click.style(path / file_name, fg='green')}."
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
    """Shows the list of found jobs."""
    show_jobs_info(
        classes=load_jobs(path),
        path=path,
        verbose=True,
        logger=make_default_logger(use_ansi=True, fmt=empty_log_format),
    )

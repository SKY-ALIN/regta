"""Production-ready scheduler with async, multithreading and multiprocessing support for Python.
See details at the repository on \n https://github.com/SKY-ALIN/regta/
"""

from typing import Callable, Tuple, Type, Union

import asyncio
import logging
from logging import Logger
from pathlib import Path

import click

from . import __version__
from .enums import CodeStyles, JobTypes
from .jobs import AsyncJob, JobHint
from .logging import empty_log_format, JobLoggerAdapter, make_default_logger, prod_log_format
from .templates import generate_decorator_styled_job, generate_oop_styled_job
from .utils import load_jobs, load_object, run_jobs, show_jobs_info

logger_param_help = (
    "Path to logger factory in the following format: "
    "<module>:<logger_factory>. Example: `src.logger:make_jobs_logger`."
)
verbose_param_help = "Set DEBUG level to logger."
no_ansi_param_help = "Disable ANSI colors."
path_param_help = "Path to directory with jobs."
job_type_param_help = "Job type. Defines how the job will use system resources."
code_style_param_help = "Job code style."


def _get_loggers(logger_uri: str, use_ansi: bool, verbose: bool) -> Tuple[Logger, JobLoggerAdapter]:
    logger_factory: Union[Callable[[], Logger], None] = load_object(logger_uri) if logger_uri else None
    logger: Logger = (
        logger_factory()
        if logger_factory
        else make_default_logger(use_ansi=use_ansi, fmt=prod_log_format)
    )

    if verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    wrapped_logger = JobLoggerAdapter(
        logger,
        plain_job_name='regta',
        styled_job_name=click.style('regta', fg='magenta'),
        use_ansi=use_ansi,
    )
    return logger, wrapped_logger


@click.group(help=__doc__)
@click.version_option(__version__)
def main(): pass


@main.command()
@click.option(
    '--path', '-P', 'path',
    default=Path('.'),
    show_default='current directory',
    type=Path,
    help=path_param_help,
)
@click.option(
    '--logger', '-L', 'logger_uri',
    help=logger_param_help,
)
@click.option(
    '--verbose', '-V', 'verbose',
    is_flag=True,
    help=verbose_param_help,
)
@click.option(
    '--no-ansi', 'disable_ansi',
    is_flag=True,
    help=no_ansi_param_help,
)
def run(path: Path, logger_uri: str, disable_ansi: bool, verbose: bool):
    """Start all jobs."""
    use_ansi = not disable_ansi

    logger, wrapped_logger = _get_loggers(logger_uri, use_ansi, verbose)

    classes = load_jobs(path)

    show_jobs_info(classes=classes, verbose=verbose, logger=wrapped_logger, use_ansi=use_ansi)

    try:
        run_jobs(classes=classes, logger=logger, use_ansi=use_ansi)
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
    help=job_type_param_help,
)
@click.option(
    '--style', '-S', 'code_style',
    default=CodeStyles.DECORATOR.value,
    show_default=True,
    type=click.Choice([style.value for style in CodeStyles]),
    help=code_style_param_help,
)
@click.option(
    '--path', '-P', 'path',
    default=Path('jobs/'),
    show_default=True,
    type=Path,
    help=path_param_help,
)
def new(name: str, job_type: str, code_style: str, path: Path):
    """Create a new job by template."""
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
    help=path_param_help,
)
@click.option(
    '--no-ansi', 'disable_ansi',
    is_flag=True,
    help=no_ansi_param_help,
)
def list_command(path: Path, disable_ansi: bool):
    """Show the list of found jobs."""
    show_jobs_info(
        classes=load_jobs(path),
        path=path,
        verbose=True,
        logger=make_default_logger(use_ansi=not disable_ansi, fmt=empty_log_format),
    )


@main.command()
@click.argument('job_uri')
@click.option(
    '--logger', '-L', 'logger_uri',
    help=logger_param_help,
)
@click.option(
    '--verbose', '-V', 'verbose',
    is_flag=True,
    help=verbose_param_help,
)
@click.option(
    '--no-ansi', 'disable_ansi',
    is_flag=True,
    help=no_ansi_param_help,
)
def execute(job_uri: str, logger_uri: str, verbose: bool, disable_ansi: bool):
    """Execute a single job once and immediately.

    JOB_URI - path to the job in following format: <module>:<job>. Example: `jobs.database_jobs:make_backup`.
    """
    use_ansi = not disable_ansi

    logger, wrapped_logger = _get_loggers(logger_uri, use_ansi, verbose)

    job_class: Type[JobHint] = load_object(job_uri)
    job: JobHint = job_class(logger=logger, use_ansi=use_ansi)

    job_name = job.get_styled_job_name() if use_ansi else job.get_plain_job_name()
    wrapped_logger.warning("Manually initiated execution of %s", job_name)

    if isinstance(job, AsyncJob):
        asyncio.run(job.execute())
    else:
        job.execute()

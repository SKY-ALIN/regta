from typing import Any, Iterable, List, Sequence, Type, Union

from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
import inspect
from logging import Logger, LoggerAdapter
from pathlib import Path
import re
import string

import click

from .jobs import JobHint, jobs_classes
from .schedulers import Scheduler


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


def show_jobs_info(
        logger: Union[Logger, LoggerAdapter],
        jobs: Sequence[JobHint] = (),
        classes: Sequence[Type[JobHint]] = (),
        path: Union[Path, None] = None,
        verbose: bool = False,
        use_ansi: bool = True,
):
    jobs_count = (len(jobs)+len(classes))
    end_char = ':' if verbose and jobs_count > 0 else '.'
    count = click.style(
        jobs_count,
        fg='green' if jobs_count > 0 else 'red',
    ) if use_ansi else jobs_count
    path_str = (
        (f" at {click.style(f'{path}/', fg='green')}" if use_ansi else f" at {path}/")
        if path is not None
        else ""
    )
    logger.info(f"[{count}] jobs were found{path_str}{end_char}")

    if verbose:
        for _class in sorted(list(classes) + [job.__class__ for job in jobs], key=lambda _class: _class.__name__):
            logger.info(f"* {_class.get_styled_job_name() if use_ansi else _class.get_plain_job_name()}")


def load_jobs(path: Path) -> List[Type[JobHint]]:
    jobs: List[Type[JobHint]] = []
    for file in path.glob('**/*.py'):
        if file.parts[0][0] == '.':  # skip hidden
            continue

        module_name = ".".join(file.with_suffix("").parts)
        spec = spec_from_file_location(module_name, file)
        if spec is None or spec.loader is None:
            continue
        module = module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore

        jobs.extend(
            cls[1]
            for cls
            in inspect.getmembers(module, inspect.isclass)
            if issubclass(cls[1], tuple(jobs_classes.values()))
            and cls[0] not in (job_class.__name__ for job_class in jobs_classes.values())
        )
    return jobs


def load_object(uri: str) -> Any:
    module_name, object_name = uri.split(':')
    module = import_module(module_name)
    return getattr(module, object_name)


def run_jobs(
        jobs: Iterable[JobHint] = (),
        classes: Iterable[Type[JobHint]] = (),
        logger: Union[Logger, None] = None,
        use_ansi: bool = True,
):
    """Initializes :class:`regta.Scheduler` and starts passed jobs.

    Args:
        jobs: List of job instances.
        classes: List of job classes. This func will make instances from them.
        logger: If a logger isn`t passed, regta will use std output.
        use_ansi: Enable / Disable ANSI colors.

    Raises:
        ValueError: If jobs or classes weren't passed.
    """
    if not jobs and not classes:
        raise ValueError("Jobs or jobs classes missed")

    scheduler = Scheduler()
    for job in jobs:
        job.logger = logger
        scheduler.add_job(job)
    for job_class in classes:
        scheduler.add_job(job_class(logger=logger, use_ansi=use_ansi))
    scheduler.run(block=True)

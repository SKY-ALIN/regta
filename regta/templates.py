from typing import Tuple

from pathlib import Path
import random

from jinja2 import Environment, PackageLoader, select_autoescape

from .enums import DecoratorNames, JobTypes
from .jobs import jobs_classes
from .utils import add_init_file, to_camel_case, to_snake_case

env = Environment(
    loader=PackageLoader("regta"),
    autoescape=select_autoescape(),
)


class Templates:
    CLASS_JOB = env.get_template("class_job.template")
    DECORATOR_JOB = env.get_template("decorator_job.template")


def _fix_job_name(name: str) -> str:
    if name[-3:].lower() != 'job':
        name += "-job"
    return name


def _generate_job(name: str, path: Path, template: str) -> str:
    file_name = f"{to_snake_case(name)}.py"

    path.mkdir(parents=True, exist_ok=True)
    add_init_file(path)
    with open(path / file_name, 'w', encoding='utf-8') as job_file:
        job_file.write(template)

    return file_name


def generate_oop_styled_job(name: str, job_type: JobTypes, path: Path) -> Tuple[str, str]:
    name = _fix_job_name(name)

    class_name = to_camel_case(name)
    template = Templates.CLASS_JOB.render(
        job_class=jobs_classes[job_type].__name__,
        class_name=class_name,
        is_async=(job_type == JobTypes.ASYNC),
        seconds=random.randint(2, 60),
    )

    file_name = _generate_job(name, path, template)

    return file_name, class_name


def generate_decorator_styled_job(name: str, job_type: JobTypes, path: Path) -> Tuple[str, str]:
    name = _fix_job_name(name)

    function_name = to_snake_case(name)
    template = Templates.DECORATOR_JOB.render(
        decorator_name=DecoratorNames(job_type).name,
        function_name=function_name,
        is_async=(job_type == JobTypes.ASYNC),
        seconds=random.randint(2, 60),
    )

    file_name = _generate_job(name, path, template)

    return file_name, function_name

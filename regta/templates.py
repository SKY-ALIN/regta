from pathlib import Path
from typing import Tuple
import random

from jinja2 import Environment, PackageLoader, select_autoescape

from .jobs import jobs_classes
from .enums import JobTypes
from .utils import (
    to_snake_case,
    to_camel_case,
    add_init_file,
)

env = Environment(
    loader=PackageLoader("regta"),
    autoescape=select_autoescape(),
)


class Templates:
    CLASS_JOB = env.get_template("class_job.template")


def generate_job(name: str, job_type: JobTypes, path: Path) -> Tuple[str, str]:
    if name[-3:].lower() != 'job':
        name += "-job"
    file_name = f"{to_snake_case(name)}.py"
    class_name = to_camel_case(name)

    template = Templates.CLASS_JOB
    path.mkdir(parents=True, exist_ok=True)
    add_init_file(path)
    with open(path / file_name, 'w') as job_file:
        job_file.write(template.render(
            job_class=jobs_classes[job_type].__name__,
            class_name=class_name,
            is_async=(job_type == JobTypes.ASYNC),
            seconds=random.randint(2, 60),
        ))

    return file_name, class_name

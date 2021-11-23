from enum import Enum

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("regta"),
    autoescape=select_autoescape(),
)


class JobTypes(Enum):
    ASYNC = 'async'
    THREAD = 'thread'
    PROCESS = 'process'


job_templates = {
    JobTypes.ASYNC: env.get_template("async_job.template"),
    JobTypes.THREAD: env.get_template("thread_job.template"),
    JobTypes.PROCESS: env.get_template("process_job.template"),
}

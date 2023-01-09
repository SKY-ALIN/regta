from typing import Dict

from logging import basicConfig, Formatter, INFO, Logger, LoggerAdapter, StreamHandler
import sys
import traceback

from click import style
from click.utils import auto_wrap_for_ansi, resolve_color_default, should_strip_ansi, strip_ansi, WIN

log_format = '%(asctime)s [%(job)s] [%(levelname)s] - %(message)s'
basicConfig(format=log_format)


class BorgSingletonMeta(type):
    _instances: Dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ClickFormatter(Formatter):
    def formatException(self, ei) -> str:
        exc_class, exc_info, exc_traceback = ei
        return (
            style("".join(traceback.format_tb(exc_traceback)), fg='yellow')
            + style(f'{exc_class.__name__}: {str(exc_info)}', fg='red')
        )


class ClickStreamHandler(StreamHandler, metaclass=BorgSingletonMeta):
    def __init__(self, use_ansi: bool):
        super().__init__(stream=sys.stdout)
        self.use_ansi = use_ansi

    def emit(self, record):
        try:
            out = self.format(record) + self.terminator
            stream = self.stream

            color = resolve_color_default(color=self.use_ansi)
            if should_strip_ansi(stream, color):
                out = strip_ansi(out)
            elif WIN:
                if auto_wrap_for_ansi is not None:
                    stream = auto_wrap_for_ansi(stream)  # type: ignore
                elif not color:
                    out = strip_ansi(out)

            stream.write(out)
            self.flush()
        except RecursionError:
            raise
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)


class DefaultLogger(Logger, metaclass=BorgSingletonMeta):
    pass


def make_default_logger(use_ansi: bool) -> DefaultLogger:
    formatter = ClickFormatter(log_format)

    handler = ClickStreamHandler(use_ansi=use_ansi)
    handler.setLevel(INFO)
    handler.setFormatter(formatter)

    logger = DefaultLogger(__name__, level=INFO)
    logger.addHandler(handler)
    return logger


class JobLoggerAdapter(LoggerAdapter):
    def __init__(self, logger: Logger, job, use_ansi: bool):
        job_name = job.styled_str() if use_ansi else str(job)
        extra = {
            "job": job_name,
        }
        super().__init__(logger=logger, extra=extra)

import logging


def logger_factory():
    level = logging.INFO

    formatter = logging.Formatter('%(asctime)s [%(job)s] [%(levelname)s] - %(message)s')

    handler = logging.FileHandler('output.log')
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

FROM python:3.9-buster

WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Instal dependencies
RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

COPY ./ ./
CMD ["regta", "run", "--path", "jobs/", "--verbose", "--logger", "logger:logger_factory"]

FROM python:3.9-buster

WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Instal dependencies using poetry
RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

# Copy project's files
COPY ./ ./

# Start regta with verbose output
CMD ["regta", "run", "--path", "jobs/", "--verbose", "--logger", "logger:logger_factory"]

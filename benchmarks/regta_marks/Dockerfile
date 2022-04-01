FROM python:3.9-buster

WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

RUN pip install regta

COPY ./ ./

ARG JOBS_AMOUNT
ENV JOBS_AMOUNT $JOBS_AMOUNT
ARG JOBS_TYPE
ENV JOBS_TYPE $JOBS_TYPE

RUN python generate_jobs.py

CMD ["regta", "run"]

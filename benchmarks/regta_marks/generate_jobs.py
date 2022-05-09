import os
from pathlib import Path

from regta.templates import generate_oop_styled_job
from regta.enums import JobTypes

JOBS_AMOUNT = int(os.getenv("JOBS_AMOUNT"))
JOBS_TYPE = JobTypes(os.getenv("JOBS_TYPE"))
PATH = Path('jobs/')


def main():
    for i in range(1, JOBS_AMOUNT+1):
        job_name = f"n_{i}_job"
        file_name, class_name = generate_oop_styled_job(job_name, JOBS_TYPE, PATH)
        print(f"Job {class_name} generated at {PATH / file_name}.")


if __name__ == "__main__":
    main()

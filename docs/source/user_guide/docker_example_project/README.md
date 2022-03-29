## Regta docker example

All jobs are very simple and auto generated.

Type `docker-compose build periodic_jobs && docker-compose up periodic_jobs` to build and start container

To check log file enter into container using `docker exec -ti docker_example_project_periodic_jobs_1 bash`,
after type `cat output.log` to show file.
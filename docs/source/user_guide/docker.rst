Docker Example
==============
Let's check how to setup regta with docker. For this example we wrote a
`little basic example project <link-to-project_>`_.

.. literalinclude:: docker_example_project/Dockerfile
   :language: Docker
   :caption: Dockerfile

Example's files Structure
-------------------------

.. code-block:: none

    docker_example_project
    ├── Dockerfile
    ├── README.md
    ├── docker-compose.yaml
    ├── jobs
    │   ├── __init__.py
    │   ├── first_job.py
    │   ├── second_job.py
    │   └── third_job.py
    ├── logger.py
    └── pyproject.toml

.. literalinclude:: docker_example_project/pyproject.toml
   :language: TOML
   :caption: pyproject.toml | File with dependencies

.. literalinclude:: docker_example_project/logger.py
   :language: python
   :caption: logger.py | File with logger factory

.. seealso::
   Full example with all files is hosted in
   `docs/source/user_guide/docker_example_project <link-to-project_>`_.

.. _link-to-project: https://github.com/SKY-ALIN/regta/tree/main/docs/source/user_guide/docker_example_project

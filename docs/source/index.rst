Overview
========

**Regta** is a production-ready scheduler with async, multithreading and multiprocessing support for Python.

.. image:: https://img.shields.io/pypi/pyversions/regta.svg
   :target: https://github.com/SKY-ALIN/regta

.. image:: https://github.com/SKY-ALIN/regta/actions/workflows/code-quality.yml/badge.svg
   :target: https://github.com/SKY-ALIN/regta

.. image:: https://badge.fury.io/py/regta.svg
   :target: https://pypi.org/project/regta/

.. image:: https://img.shields.io/github/license/SKY-ALIN/regta.svg
   :target: https://github.com/SKY-ALIN/regta/blob/main/LICENSE

.. seealso::
   You can find out how and why to use various job types
   :ref:`here <jobs-types>`.

Core Features
-------------

**Various job types**
  Create async, thread-based, or process-based jobs depending on your goals.

**Flexible Intervals**
  Use standard `timedelta` object or specially designed `Period` for highly responsible jobs.

**Multi-Paradigm**
  Design OOP styled or functional styled jobs.

**CLI Interface**
  Regta provides a CLI tool to start, list and create jobs by template.

**Professional Logging**
  Redefine standard logger and define your own. ANSI coloring is supported.


Check :ref:`quick-start` to start

.. toctree::
   :maxdepth: 2
   :caption: Contents
   :hidden:

   self
   User Guide <user_guide/index>
   api_reference
   cli_reference

.. toctree::
   :caption: Development
   :hidden:

   changelog
   license
   GitHub Repository <https://github.com/SKY-ALIN/regta>
   PyPI Page <https://pypi.org/project/regta/>

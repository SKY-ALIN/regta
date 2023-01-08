Overview
========

**Regta** is a production-ready scheduler with async, multithreading and multiprocessing support for Python.

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
  Design OOP styled or functional styled jobs. Also, Regta provides an interface to reuse
  already written code by a config.

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

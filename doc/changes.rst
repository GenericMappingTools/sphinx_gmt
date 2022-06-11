.. _changes:

Changelog
=========

v0.3.0 (2022/05/01)
-------------------

* Add examples for including GMT classic and modern scripts
* Fix the missing "type_ignores" exception for Python scripts
* Setting ``GMT_END_SHOW`` to ``off`` to disable image display in external viewers
* Add labels to images so that they can be referenced

v0.2.0 (2022/04/26)
-------------------

* Images and scripts are named based on the code's md5sum
* Bump the minimum required Python version to 3.8
* Change the default branch from ``master`` to ``main``
* Migrate CI from Azure Pipelines and Travics to GitHub Actions
* Switch from versioneer to setuptools_scm for version management

v0.1.1 (2019/09/16)
-------------------

* Disable displaying figure when ``gmt end show`` is used (#26)

v0.1.0 (2019/06/21)
-------------------

* First release of ``sphinx_gmt`` with the ``gmtplot`` directive for automatically
  generating GMT plots and inserting them into Sphinx generated documentation. Supports
  multiple GMT versions, bash, and Python (through PyGMT).

.. title:: sphinx_gmt

Sphinx extensions for the Generic Mapping Tools
===============================================

This package provdes a `Sphinx <http://www.sphinx-doc.org/>`__ extension for
including `GMT <http://gmt.soest.hawaii.edu/>`__ codes and figures in your
documentation. The extension defines the ``gmt-plot`` directive that
will execute the given code and insert the generated figure into the document.

Features
--------

- Support any versions of GMT
- Support both Bash and Python (including `PyGMT <https://www.pygmt.org/>`__) scripts
- Support both inline codes and loading codes from a script
- Options to show/hide the codes and link to codes if codes are hidden

.. toctree::
    :maxdepth: 2
    :caption: Documentation

    install.rst
    gmtplot.rst
    api.rst


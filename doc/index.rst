.. title:: sphinx_gmt

Sphinx extensions for the Generic Mapping Tools
===============================================

Convert this:

.. code::

   .. gmt-plot::
       :language: bash
       :show-code: false

       gmt grdimage @earth_relief_15m.grd -Rg -JW10i -Baf -Cgeo > global_relief.ps

into this:

.. gmt-plot::
    :language: bash
    :show-code: false
    :caption: GMT plot automatically generated and included by the sphinx extension 🚀

    gmt grdimage @earth_relief_15m.grd -Rg -JW10i -Baf -Cgeo > global_relief.ps

.. include:: ../README.rst
    :start-after: placeholder-for-doc-index

.. toctree::
    :maxdepth: 2
    :caption: Documentation
    :hidden:

    install.rst
    gmtplot.rst
    api/index.rst


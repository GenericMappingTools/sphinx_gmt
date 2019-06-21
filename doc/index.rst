.. title:: sphinx_gmt

Sphinx extensions for the Generic Mapping Tools
===============================================

Convert this:

.. code::

   .. gmtplot::
       :language: bash
       :show-code: false

       gmt pscoast -Rg -JW10i -Baf -Ggray > globe.ps

into this:

.. gmtplot::
    :language: bash
    :show-code: false
    :caption: GMT plot automatically generated and included by the sphinx extension 🚀

    gmt pscoast -Rg -JW10i -Baf -Ggray > globe.ps

.. include:: ../README.rst
    :start-after: placeholder-for-doc-index

.. toctree::
    :maxdepth: 2
    :caption: Documentation
    :hidden:

    install.rst
    gmtplot.rst
    api/index.rst
    releases.rst
    changes.rst


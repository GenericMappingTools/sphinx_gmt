.. _install:

Installing
==========


Which Python?
-------------

You'll need **Python 3.7 or greater** to use this extension.


Dependencies
------------

* `GMT <http://gmt.soest.hawaii.edu/>`__
* `sphinx <http://www.sphinx-doc.org>`__
* `jinja2 <http://jinja.pocoo.org/>`__


Installing with conda
---------------------

You can install ``sphinx_gmt`` using the `conda package manager <https://conda.io/>`__
that comes with the Anaconda distribution::

    conda install sphinx_gmt --channel conda-forge


Installing with pip
-------------------

Alternatively, you can also use the `pip package manager <https://pypi.org/project/pip/>`__::

    pip install sphinx_gmt


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest source from GitHub::

    pip install https://github.com/GenericMappingTools/sphinx_gmt/archive/main.zip

Alternatively, you can clone the git repository locally and install from there::

    git clone https://github.com/GenericMappingTools/sphinx_gmt.git
    cd sphinx_gmt
    pip install .


Enabling the extensions
-----------------------

After installing the Python package, you'll have to enable each extension in your
``conf.py`` file:

.. code:: python

    extensions = [
        ...,
        "sphinx_gmt.gmtplot",
    ]


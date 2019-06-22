.. _install:

Installing
==========


Which Python?
-------------

You'll need **Python 3.6 or greater** to use this extension.


Dependencies
------------

* `GMT <http://gmt.soest.hawaii.edu/>`__
* `sphinx <http://www.sphinx-doc.org>`__
* `jinja2 <http://jinja.pocoo.org/>`__


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest source from GitHub::

    pip install https://github.com/GenericMappingTools/sphinx_gmt/archive/master.zip

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


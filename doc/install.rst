.. _install:

Installing
==========


Which Python?
-------------

You'll need **Python 3.5 or greater** to run GMT/Python.

We recommend using the `Anaconda <http://continuum.io/downloads#all>`__ Python
distribution to ensure you have all dependencies installed and the ``conda``
package manager available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


Dependencies
------------

* `GMT <http://gmt.soest.hawaii.edu/>`__
* `sphinx <http://www.sphinx-doc.org>`__
* `jinja2 <http://jinja.pocoo.org/>`__
* `ipython <https://ipython.org/>`__


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest source from Github::

    pip install https://github.com/GenericMappingTools/gmtsphinxext/archive/master.zip

Alternatively, you can clone the git repository locally and install from there::

    git clone https://github.com/GenericMappingTools/gmtsphinxext.git
    cd gmtsphinxext
    pip install .


Enabling the extensions
-----------------------

After installing the Python package, you'll have to enable each extension in your
``conf.py`` file:

.. code:: python

    extensions = [
        ...,
        "gmtsphinxext.gmtplot",
    ]


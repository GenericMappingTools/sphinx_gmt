Usage
=====

The extension defines the :mod:`~sphinx_gmt.gmtplot` directive that will execute the
given GMT codes and insert the generated figure into the document.

The GMT codes may be included in one of two ways:

1.  **A path to a source file** as the argument to the directive::

        .. gmtplot:: path/to/plot.sh

           Optional caption for the plot

    The source file name is usually relative to the current file's path.
    However, if it is an absolute path starting with ``/``, it is relative to
    the top source directory.

    In this way, the directive will try to guess the script language from its
    file suffix. Supported suffixes are ``.sh``, ``.bash`` and ``.py``.

2.  Included as **inline content** to the directive::

        .. gmtplot::
            :language: bash

            # place GMT codes here
            gmt ...
            gmt ...
            gmt ...

    In this way, you have to let it know the script language by providing
    the ``:language:`` option.

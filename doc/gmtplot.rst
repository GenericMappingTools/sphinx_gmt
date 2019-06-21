.. _sphinxext:

Including GMT Plots in Sphinx
=============================

The extension defines the ``gmt-plot`` directive that will execute the given
GMT codes and insert the generated figure into the document.

Usage
-----

The GMT codes may be included in one of two ways:

1.  **A path to a source file** as the argument to the directive::

        .. gmt-plot:: path/to/plot.sh

           Optional caption for the plot

    The source file name is usually relative to the current file's path.
    However, if it is absolute (starting with ``/``), it is relative to
    the top source directory.

    In this way, it will try to guess the script language from its file suffix.
    Supported suffixes are ``.sh``, ``.bash`` and ``.py``.

2.  Included as **inline content** to the directive::

        .. gmt-plot::
            :language: bash

            # place GMT codes here
            gmt ...
            gmt ...
            gmt ...

    In this way, you have to let it know the script language by providing
    the ``:language:`` option.


Examples
--------

The following RST code:

.. code-block:: bash

    .. gmt-plot::
        :language: bash
        :caption: Example showing how to include GMT figures with inline codes

        ps=example_05.ps
        gmt grdmath -R-15/15/-15/15 -I0.3 X Y HYPOT DUP 2 MUL PI MUL 8 DIV COS EXCH NEG 10 DIV EXP MUL = sombrero.nc
        gmt makecpt -C128 -T-5,5 -N > g.cpt
        gmt grdview sombrero.nc -JX6i -JZ2i -B5 -Bz0.5 -BSEwnZ -N-1+gwhite -Qs -I+a225+nt0.75 -X1.5i \
            -Cg.cpt -R-15/15/-15/15/-1/1 -K -p120/30 > $ps
        echo "4.1 5.5 z(r) = cos (2@~p@~r/8) @~\327@~e@+-r/10@+" | gmt pstext -R0/11/0/8.5 -Jx1i \
	        -F+f50p,ZapfChancery-MediumItalic+jBC -O >> $ps
        rm -f g.cpt sombrero.nc

is executed by sphinx and turned into:

.. gmt-plot::
    :language: bash
    :caption: Example showing how to include GMT figures with inline codes

    ps=example_05.ps
    gmt grdmath -R-15/15/-15/15 -I0.3 X Y HYPOT DUP 2 MUL PI MUL 8 DIV COS EXCH NEG 10 DIV EXP MUL = sombrero.nc
    gmt makecpt -C128 -T-5,5 -N > g.cpt
    gmt grdview sombrero.nc -JX6i -JZ2i -B5 -Bz0.5 -BSEwnZ -N-1+gwhite -Qs -I+a225+nt0.75 -X1.5i \
	    -Cg.cpt -R-15/15/-15/15/-1/1 -K -p120/30 > $ps
    echo "4.1 5.5 z(r) = cos (2@~p@~r/8) @~\327@~e@+-r/10@+" | gmt pstext -R0/11/0/8.5 -Jx1i \
	    -F+f50p,ZapfChancery-MediumItalic+jBC -O >> $ps
    rm -f g.cpt sombrero.nc

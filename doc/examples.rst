Examples
========

The ``gmtplot`` directive supports any GMT versions, and both Bash and Python
scripts.

Classic GMT bash script
-----------------------

The following RST code:

.. code-block:: bash

    .. gmtplot::
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

.. gmtplot::
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


Modern GMT bash script
----------------------

We have a modern-mode GMT bash script ``modern-gmt.sh`` in the ``examples/`` directory.
Its content is:

.. literalinclude:: examples/modern-gmt.sh

The following ReST code:

.. code-block:: bash

    .. gmtplot:: examples/modern-gmt.sh
        :width: 30%
        :caption: GMT Orthographic projection

is executed by sphinx and turned into:

.. gmtplot:: examples/modern-gmt.sh
    :width: 50%
    :caption: GMT Orthographic projection

Data files
----------

If your GMT script needs data files, you can put data files under the same
directory as the GMT script (or the ReST file for inline codes). Or you can put
data files in directories defined by environmental variable **GMT_DATADIR**.

In this example, the script is ``examples/needs-data-files.sh``, and the data
file is ``examples/points.txt``.

The following ReST code:

.. code-block:: bash

    .. gmtplot:: examples/needs-data-files.sh
        :width: 50%
        :caption: GMT script needs a data file.

is executed by sphinx and turned into:

.. gmtplot:: examples/needs-data-files.sh
    :width: 50%
    :caption: GMT script needs a data file.

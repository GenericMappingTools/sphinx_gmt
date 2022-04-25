sphinx_gmt
==========

   Sphinx extensions for the Generic Mapping Tools

`Documentation <https://www.generic-mapping-tools.org/sphinx_gmt>`__ |
`Documentation (development version) <https://www.generic-mapping-tools.org/sphinx_gmt/dev>`__ |
`Source Code <https://github.com/GenericMappingTools/sphinx_gmt>`__

.. image:: http://img.shields.io/pypi/v/sphinx_gmt.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/sphinx_gmt
.. image:: https://github.com/GenericMappingTools/sphinx_gmt/workflows/Tests/badge.svg
   :alt: GitHub Actions status
   :target: https://github.com/GenericMappingTools/sphinx_gmt/actions
.. image:: https://img.shields.io/pypi/pyversions/sphinx_gmt.svg?style=flat-square
    :alt: Compatible Python versions.
    :target: https://pypi.python.org/pypi/sphinx_gmt
.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg
    :alt: Contributor Code of Conduct
    :target: CODE_OF_CONDUCT.md

.. placeholder-for-doc-index


About
-----

This package provides a `Sphinx <http://www.sphinx-doc.org/>`__ extension for
including `GMT <http://gmt.soest.hawaii.edu/>`__ code and figures in your
documentation. The extension defines the ``gmtplot`` directive that
will execute the given code and insert the generated figure into the document
(like the `matplotlib <https://matplotlib.org/>`__ ``plot`` directive).


Features
--------

- Supports any version of GMT
- Works with both Bash and Python (`PyGMT <https://www.pygmt.org/>`__)
- Include code inline or load from a script
- Options to show/hide the code, insert captions, link to hidden code, etc.


Contacting Us
-------------

Most discussion happens
`on Github <https://github.com/GenericMappingTools/sphinx_gmt>`__.
Feel free to
`open an issue <https://github.com/GenericMappingTools/sphinx_gmt/issues/new>`__
or comment on any open issue or pull request.


Contributing
------------

Code of conduct
+++++++++++++++

Please note that this project is released with a `Contributor Code of Conduct
<https://github.com/GenericMappingTools/sphinx_gmt/blob/main/CODE_OF_CONDUCT.md>`__.
By participating in this project you agree to abide by its terms.

Contributing Guidelines
+++++++++++++++++++++++

Please read our `Contributing Guide
<https://github.com/GenericMappingTools/sphinx_gmt/blob/main/CONTRIBUTING.md>`__ to
see how you can help and give feedback.

Imposter syndrome disclaimer
++++++++++++++++++++++++++++

**We want your help.** No, really.

There may be a little voice inside your head that is telling you that you're not ready
to be an open source contributor; that your skills aren't nearly good enough to
contribute. What could you possibly offer?

We assure you that the little voice in your head is wrong.

**Being a contributor doesn't just mean writing code**.
Equality important contributions include: writing or proof-reading documentation,
suggesting or implementing tests, or even giving feedback about the project (including
giving feedback about the contribution process). If you're coming to the project with
fresh eyes, you might see the errors and assumptions that seasoned contributors have
glossed over. If you can write any code at all, you can contribute code to open source.
We are constantly trying out new skills, making mistakes, and learning from those
mistakes. That's how we all improve and we are happy to help others learn.

*This disclaimer was adapted from the*
`MetPy project <https://github.com/Unidata/MetPy>`__.


License
-------

This is free software: you can redistribute it and/or modify it under the terms
of the **BSD 3-clause License**. A copy of this license is provided in
`LICENSE.txt <https://github.com/GenericMappingTools/sphinx_gmt/blob/main/LICENSE.txt>`__.

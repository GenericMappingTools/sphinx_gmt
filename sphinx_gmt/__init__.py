"""
Sphinx extensions for GMT.
"""
from importlib.metadata import version

# Get semantic version through setuptools-scm
__version__ = f'v{version("sphinx_gmt")}'  # e.g. v0.1.2.dev3+g0ab3cd78
__commit__ = __version__.split("+g")[-1] if "+g" in __version__ else ""  # 0ab3cd78

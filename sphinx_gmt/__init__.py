"""
Sphinx extensions for GMT.
"""
from pkg_resources import get_distribution

# Get semantic version through setuptools-scm
__version__ = f'v{get_distribution("pygmt").version}'  # e.g. v0.1.2.dev3+g0ab3cd78
__commit__ = __version__.split("+g")[-1]  # 0ab3cd78

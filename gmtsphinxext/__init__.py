"""
Sphinx extensions for GMT.
"""
from ._version import get_versions as _get_versions

# Get the version number through versioneer
__version__ = _get_versions()["version"]
__commit__ = _get_versions()["full-revisionid"]

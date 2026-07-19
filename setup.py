"""Compatibility entry point for tools that still invoke ``setup.py``.

Package metadata, including runtime dependencies, lives in ``pyproject.toml``.
Keeping this file metadata-free prevents it from drifting out of sync.
"""

from setuptools import setup


setup()

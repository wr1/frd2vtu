"""
Convert CalculiX .frd files to VTK .vtu files.

This module provides functionality to convert CalculiX .frd files (binary format)
to VTK .vtu files. It supports various element types and can handle multiple files
in parallel.

Example:
    >>> from frd2vtu import frd2vtu
    >>> frd2vtu("model.frd")  # Convert single file
    >>> frd2vtu("model1.frd", "model2.frd")  # Convert multiple files
"""

from .frd2vtu import frdbin2vtu, frd2vtu

__all__ = ["frd2vtu", "frdbin2vtu"]

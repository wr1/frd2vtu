"""
Convert CalculiX .frd files to VTK .vtu files.

Binary FRD files are converted to VTK unstructured grids. Use the CLI
(``frd2vtu convert``, ``frd2vtu iprep``) or call :func:`frdbin2vtu` /
:func:`frd2vtu` from Python.

Example:
    >>> from frd2vtu import frdbin2vtu, frd2vtu
    >>> frdbin2vtu("model.frd", output_dir="out/")
    >>> frd2vtu(["model1.frd", "model2.frd"], parallel=True, output_dir="out/")
"""

from .core import frd2vtu, frdbin2vtu
from .plotting import basic_plots, plot_mesh_point_arrays

__all__ = ["basic_plots", "frd2vtu", "frdbin2vtu", "plot_mesh_point_arrays"]

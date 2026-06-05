#! /usr/bin/env python
"""
Plotting functionality for VTU files.
"""

import logging
import math
import multiprocessing
from typing import List

import numpy as np
import pyvista as pv
from treeparse import argument, cli, option

from frd2vtu._logging import configure_logging

logger = logging.getLogger(__name__)


def plot_mesh_point_arrays(vtu: str) -> None:
    """Plot point arrays from a VTU file and save as PNG."""
    if not vtu.endswith(".vtu"):
        raise ValueError("Input file must be a .vtu file.")

    mesh = pv.read(vtu)
    point_arrays = mesh.point_data

    num_arrays = len(point_arrays) - 1
    num_cols = math.ceil(math.sqrt(num_arrays))
    num_rows = math.ceil(num_arrays / num_cols)
    plotter = pv.Plotter(
        shape=(num_rows, num_cols),
        window_size=(1200 * num_cols, 800 * num_rows),
        off_screen=True,
    )

    keys = [i for i in point_arrays.keys() if i != "ccx_id"]
    fact = 1.0
    warped_mesh = mesh
    for i, array_name in enumerate(keys):
        row = i // num_cols
        col = i % num_cols
        plotter.subplot(row, col)

        if array_name.lower().find("disp") != -1:
            amax = mesh.point_data[array_name].max()
            b = np.array(mesh.bounds)
            if fact == 1:
                fact = 0.1 * b.max() / amax
            warped_mesh = mesh.warp_by_vector(array_name, factor=fact)

        plotter.add_mesh(warped_mesh, scalars=array_name, show_edges=True)
        plotter.add_mesh(mesh.outline(), color="black")
        plotter.view_isometric()
        plotter.show_axes()
        plotter.add_text(
            array_name + f" scale={fact}",
            position="upper_left",
            font_size=10,
            color="black",
        )

    of = vtu.replace(".vtu", ".png")
    plotter.screenshot(of)
    plotter.close()
    logger.info("** saved %s", of)


def basic_plots(vtu_files: List[str], parallel: bool = True) -> None:
    """Create simple plots for the given VTU files."""
    if parallel:
        with multiprocessing.Pool() as pool:
            pool.map(plot_mesh_point_arrays, vtu_files)
    else:
        for vtu in vtu_files:
            plot_mesh_point_arrays(vtu)
    logger.info("** Finished plotting.")


def plot_vtu(vtu_files: List[str], no_parallel: bool = False) -> None:
    basic_plots(vtu_files, parallel=not no_parallel)


app = cli(
    name="frd2vtu_plot",
    help="Create PNG plots from VTU point data.",
    callback=plot_vtu,
    arguments=[
        argument(
            name="vtu_files",
            nargs="*",
            arg_type=str,
            help="VTU files to plot",
        ),
    ],
    options=[
        option(
            flags=["--no-parallel", "-n"],
            flag=True,
            help="Disable parallel processing",
        ),
    ],
)


def main() -> None:
    configure_logging()
    app.run()


if __name__ == "__main__":
    main()

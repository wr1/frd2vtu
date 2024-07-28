#! /usr/bin/env python

import pyvista as pv
import fire
import numpy as np
import math
import multiprocessing


def plot_mesh_point_arrays(vtu):
    # Load a mesh file (replace 'your_mesh_file.vtk' with your actual file)
    if not vtu.endswith(".vtu"):
        raise ValueError("Input file must be a .vtu file.")

    mesh = pv.read(vtu)

    # Get point arrays
    point_arrays = mesh.point_data

    num_arrays = len(point_arrays) - 1
    num_cols = math.ceil(math.sqrt(num_arrays))
    num_rows = math.ceil(num_arrays / num_cols)
    # Initialize the plotter with a split window
    plotter = pv.Plotter(
        shape=(num_rows, num_cols),
        window_size=(1200 * num_cols, 800 * num_rows),
        off_screen=True,
    )

    keys = [i for i in point_arrays.keys() if i != "ccx_id"]

    fact = 1.0

    warped_mesh = mesh
    # Iterate over point arrays and plot each in a separate subplot
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
        # plotter.add_title(array_name, font_size=10, position="upper_left")

    # Render the plots and save to a PNG file
    of = vtu.replace(".vtu", ".png")
    plotter.screenshot(of)
    plotter.close()
    print(f"** saved {of}")

    del plotter, mesh, warped_mesh


def basic_plots(*vtu):
    """
    Create simple plots for the given VTU files.

    Parameters:
        *vtu: Variable number of VTU file paths.

    Returns:
        None
    """
    p = multiprocessing.Pool()
    p.map(plot_mesh_point_arrays, vtu)
    p.close()


def main():
    fire.Fire(basic_plots)


if __name__ == "__main__":
    main()

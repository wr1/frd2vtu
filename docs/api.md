# API Reference

## frd2vtu

### `frd2vtu.frd2vtu(frd_files, parallel=True)`

Convert one or more `.frd` files to `.vtu` format.

- **Args**:
  - `*frd_files` (str): Paths to `.frd` files to convert.
  - `parallel` (bool): Use parallel processing (default: True).

- **Returns**:
  - None

### `frd2vtu.frdbin2vtu(file_path)`

Convert a single binary `.frd` file to `.vtu` format.

- **Args**:
  - `file_path` (str): Path to the input `.frd` file.

- **Returns**:
  - `pyvista.UnstructuredGrid` if successful, `None` otherwise.

## frd2vtu.basic_plot

### `frd2vtu.basic_plot.basic_plots(*vtu)`

Create simple plots for the given `.vtu` files.

- **Args**:
  - `*vtu`: Variable number of `.vtu` file paths.

- **Returns**:
  - None (saves PNG files).
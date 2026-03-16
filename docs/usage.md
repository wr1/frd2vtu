# Usage

The `frd2vtu` tool provides a command-line interface to convert `.frd` files to `.vtu` format and prepare `.inp` files.

### Basic Conversion

Convert a single `.frd` file:

```bash
frd2vtu convert input.frd
```

### Multiple Files

Convert multiple files at once (processed in parallel by default):

```bash
frd2vtu convert file1.frd file2.frd file3.frd
```

### Output Directory

Write `.vtu` files to a specific directory:

```bash
frd2vtu convert input.frd --output-dir ./results
```

### Disable Parallel Processing

```bash
frd2vtu convert file1.frd file2.frd --no-parallel
```

### Prepare Input File for Binary Output

Modify a CalculiX `.inp` file to request binary output:

```bash
frd2vtu iprep input.inp
```

Optionally specify an output directory:

```bash
frd2vtu iprep input.inp --output-dir ./prepared
```

### Plotting

Generate plots from `.vtu` files (one PNG per file, saved alongside the VTU):

```bash
frd2vtu_plot output.vtu
```

Multiple files in parallel:

```bash
frd2vtu_plot file1.vtu file2.vtu
```

Disable parallel processing:

```bash
frd2vtu_plot file1.vtu file2.vtu --no-parallel
```

For more details, see the [API Reference](api.md).

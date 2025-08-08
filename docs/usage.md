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

### Disable Parallel Processing

```bash
frd2vtu convert file1.frd file2.frd --no-parallel
```

### Prepare Input File for Binary Output

Modify a CalculiX `.inp` file to request binary output:

```bash
frd2vtu iprep input.inp
```

### Plotting

Generate basic plots from `.vtu` files:

```bash
frd2vtu_plot output.vtu
```

For more details, see the [API Reference](api.md).

# Usage

The `frd2vtu` tool provides a command-line interface to convert `.frd` files to `.vtu` format.

### Basic Conversion

Convert a single `.frd` file:

```bash
frd2vtu input.frd
```

### Multiple Files

Convert multiple files at once (processed in parallel by default):

```bash
frd2vtu file1.frd file2.frd file3.frd
```

### Plotting

Generate basic plots from `.vtu` files:

```bash
frd2vtu_plot output.vtu
```

For more details, see the [API Reference](api.md).
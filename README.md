# FRD2VTU

A Python tool to convert CalculiX .frd files to VTK .vtu files.

## Overview

This tool converts CalculiX binary .frd files to VTK .vtu files, which can be visualized in tools like ParaView. It supports various element types and can handle multiple files in parallel.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/frd2vtu.git
cd frd2vtu

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Usage

### Command Line

```bash
# Convert a single file
python -m frd2vtu.frd2vtu model.frd

# Convert multiple files
python -m frd2vtu.frd2vtu model1.frd model2.frd

# Convert multiple files in parallel (default)
python -m frd2vtu.frd2vtu model1.frd model2.frd model3.frd

# Convert multiple files sequentially
python -m frd2vtu.frd2vtu model1.frd model2.frd --parallel=False
```

### Python API

```python
# Convert a single file
from frd2vtu import frd2vtu
frd2vtu("model.frd")

# Convert multiple files
frd2vtu("model1.frd", "model2.frd")

# Convert multiple files with parallel processing disabled
frd2vtu("model1.frd", "model2.frd", parallel=False)

# Use the lower-level function directly
from frd2vtu import frdbin2vtu
grid = frdbin2vtu("model.frd")
```

## Testing

The project includes a comprehensive test suite using pytest. You can run the tests using the provided Makefile targets:

```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Run tests with coverage report
make test-coverage

# Run tests for specific file categories
make test-small    # Small files
make test-medium   # Medium files
make test-large    # Large files
make test-special  # Special cases
```

## Supported Element Types

The tool supports the following CalculiX element types:

- Hexahedron (8-node)
- Quadratic Hexahedron (20-node)
- Tetrahedron (4-node)
- Quadratic Tetrahedron (10-node)
- Prism (6-node)
- Pentahedron (15-node)
- Triangle (3-node)
- Quadratic Triangle (6-node)
- Quad (4-node)
- Quadratic Quad (8-node)
- Line (2-node)
- Quadratic Line (3-node)

## License

[MIT License](LICENSE)

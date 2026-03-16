# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Summary

**frd2vtu** converts CalculiX binary `.frd` result files to VTK `.vtu` files for visualization in ParaView. It supports 12 element types (hexahedra, prisms, tetrahedra, triangles, quads, lines, and their quadratic variants).

## Commands

```bash
# Install in editable mode with dev deps
uv pip install -e ".[dev]"

# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run a single test file
pytest test/test_frd2vtu.py -v

# Run tests for a specific FRD file (parametrized by file stem)
pytest test/test_frd2vtu.py -k "beamf"

# CLI usage
frd2vtu convert file.frd --output-dir out/
frd2vtu iprep file.inp
frd2vtu_plot out/file.vtu
```

Tests require a display for headless VTK rendering — in CI this is handled by Xvfb. Locally, ensure `DISPLAY` is set or use a virtual framebuffer.

## Architecture

```
frd2vtu/
├── core.py      — binary parsing and conversion engine
├── cli.py       — CLI entry points via treeparse framework
├── plotting.py  — PyVista-based visualization/PNG generation
└── __init__.py  — public API exports
```

### Conversion Pipeline (`core.py`)

1. **`split_blocks(buf)`** — regex-splits the binary FRD buffer into logical sections (nodes, elements, results, footer). Returns `None` for non-binary files.
2. **`frdbin2vtu(file_path, output_dir)`** — main converter: extracts node coordinates and IDs via numpy structured arrays, parses element connectivity by type, builds a PyVista `UnstructuredGrid`, attaches point/cell data arrays named `{field}_{timestamp:.3f}`, and writes `.vtu`.
3. **`frd2vtu(frd_files, parallel, output_dir)`** — batch wrapper using `multiprocessing.Pool`.

**Element type map** (`e2nn`): maps CalculiX element IDs (1–12) to node counts.

**Key implementation details:**
- Quadratic hexahedra (type 4) require node reordering from CalculiX to VTK order: `nz[e[:12] + e[16:] + e[12:16]]`
- Point data arrays are zero-padded when node IDs have gaps
- Arrays named NORM, SENMISE, SENPS1, SDV are skipped during field extraction
- Timestamp parsing starts at character position 12 to handle format variations

### Testing (`test/test_frd2vtu.py`)

All 144+ `.frd` files in `test/frds/` are parametrized as fixtures. Unsupported element types are marked `xfail`. Tests verify: valid PyVista grid output, VTU readability, PNG plot generation, and CLI help.

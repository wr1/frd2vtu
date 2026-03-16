#!/usr/bin/env python
"""Pytest tests for frd2vtu conversion functionality."""

import pytest
from pathlib import Path
import frd2vtu
import frd2vtu.plotting
import frd2vtu.cli
import pyvista as pv

TEST_DIR = Path(__file__).parent / "frds"

FRD_FILES = [
    "simplebeam.frd",
    "truss.frd",
    "oneel.frd",
    "shell7.frd",
    "contact11.frd",
    "planestress3.frd",
    "thermomech.frd",
    "concretebeam.frd",
    "contact19.frd",
    "segmentunsmooth.frd",  # complex geometry
    "induction.frd",  # large, mixed element types
]


@pytest.fixture(scope="module", params=FRD_FILES)
def grid(request):
    frd_path = TEST_DIR / request.param
    return request.param, frd2vtu.frdbin2vtu(str(frd_path))


def test_conversion(grid):
    """Converted result is a non-empty PyVista grid with expected arrays."""
    file, result = grid
    assert isinstance(result, pv.UnstructuredGrid), f"{file}: not a PyVista grid"
    assert result.n_points > 0, f"{file}: no points"
    assert result.n_cells > 0, f"{file}: no cells"
    assert "ccx_id" in result.point_data, f"{file}: missing point ccx_id"
    assert "ccx_id" in result.cell_data, f"{file}: missing cell ccx_id"
    assert "ccx_mat" in result.cell_data, f"{file}: missing cell ccx_mat"


def test_vtu_readable(grid):
    """VTU file written alongside the FRD is readable."""
    file, _ = grid
    vtu_path = TEST_DIR / Path(file).with_suffix(".vtu")
    assert vtu_path.exists(), f"{file}: VTU not created"
    assert isinstance(pv.read(vtu_path), pv.UnstructuredGrid)


def test_basic_plot(tmp_path):
    """Plotter writes a PNG next to the VTU."""
    frd_path = TEST_DIR / "simplebeam.frd"
    vtu_path = tmp_path / "simplebeam.vtu"
    result = frd2vtu.frdbin2vtu(str(frd_path))
    result.save(str(vtu_path))
    frd2vtu.plotting.plot_mesh_point_arrays(str(vtu_path))
    assert vtu_path.with_suffix(".png").exists()


def test_cli_help(monkeypatch, capsys):
    """CLI --help exits cleanly and mentions the tool."""
    monkeypatch.setattr("sys.argv", ["frd2vtu", "--help"])
    with pytest.raises(SystemExit):
        frd2vtu.cli.main()
    captured = capsys.readouterr()
    assert "Convert CalculiX .frd files" in captured.out

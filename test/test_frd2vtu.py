#!/usr/bin/env python
"""Pytest tests for frd2vtu conversion functionality."""

import logging
from pathlib import Path

import frd2vtu
import frd2vtu.cli
import frd2vtu.core
import frd2vtu.plotting
import numpy as np
import pyvista as pv
import pytest

from frd_cases import FRDS_DIR, frd_params

logger = logging.getLogger(__name__)

TEST_DIR = FRDS_DIR


@pytest.fixture(scope="module", params=list(frd_params()))
def grid(request):
    frd_name = request.param
    frd_path = TEST_DIR / frd_name
    logger.info("converting %s", frd_name)
    result = frd2vtu.frdbin2vtu(str(frd_path))
    if result is None:
        pytest.fail(f"{frd_name}: conversion returned None")
    logger.info("OK %s", frd_name)
    return frd_name, result


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


def test_frdbin2vtu_missing_file():
    """frdbin2vtu returns None when the file cannot be read."""
    result = frd2vtu.frdbin2vtu("/nonexistent/path/file.frd")
    assert result is None


def test_frd2vtu_empty():
    """frd2vtu with empty list returns without error."""
    frd2vtu.frd2vtu([], parallel=False)


def test_frd2vtu_parallel(tmp_path):
    """frd2vtu with parallel=True processes files without error."""
    files = [str(TEST_DIR / "simplebeam.frd"), str(TEST_DIR / "beamf.frd")]
    frd2vtu.frd2vtu(files, parallel=True, output_dir=str(tmp_path))
    assert (tmp_path / "simplebeam.vtu").exists()
    assert (tmp_path / "beamf.vtu").exists()


def test_frd2vtu_sequential(tmp_path):
    """frd2vtu with parallel=False processes files sequentially."""
    files = [str(TEST_DIR / "simplebeam.frd")]
    frd2vtu.frd2vtu(files, parallel=False, output_dir=str(tmp_path))
    assert (tmp_path / "simplebeam.vtu").exists()


def test_unknown_element_type(tmp_path):
    """Unsupported element type id stops parsing; earlier cells are kept."""
    coords = [
        (1, 0.0, 0.0, 0.0),
        (2, 1.0, 0.0, 0.0),
        (3, 0.0, 1.0, 0.0),
        (4, 0.0, 0.0, 1.0),
    ]
    buf = _make_frd_buffer(coords, [(1, 3, 1, [1, 2, 3, 4]), (2, 99, 1, [1, 2, 3])])
    frd_path = tmp_path / "mixed_unknown.frd"
    frd_path.write_bytes(buf)
    result = frd2vtu.frdbin2vtu(str(frd_path), str(tmp_path))
    assert result is not None
    assert result.n_cells == 1


def test_triangle_element(tmp_path):
    """Triangle elements (nid=7) convert to VTK triangles."""
    coords = [(1, 0.0, 0.0, 0.0), (2, 1.0, 0.0, 0.0), (3, 0.0, 1.0, 0.0)]
    buf = _make_frd_buffer(coords, [(1, 7, 1, [1, 2, 3])])
    frd_path = tmp_path / "triangle.frd"
    frd_path.write_bytes(buf)
    result = frd2vtu.frdbin2vtu(str(frd_path), str(tmp_path))
    assert result is not None
    assert result.n_cells == 1
    assert result.n_points == 3


def test_prepare_inp_for_binary(tmp_path):
    """prepare_inp_for_binary rewrites *node file/*el file keywords."""
    inp = tmp_path / "test.inp"
    inp.write_text("*Node File\n*El File, output=3d\n*Step\n")
    frd2vtu.core.prepare_inp_for_binary([str(inp)], output_dir=str(tmp_path))
    out = (tmp_path / "test.inp").read_text()
    assert "*node output" in out
    assert "*element output" in out
    assert "*node file" not in out.lower() or "*node output" in out


def test_prepare_inp_no_changes(tmp_path):
    """prepare_inp_for_binary skips files with no file keywords."""
    inp = tmp_path / "nochange.inp"
    inp.write_text("*Step\n*Static\n")
    frd2vtu.core.prepare_inp_for_binary([str(inp)], output_dir=str(tmp_path))
    # No output file written when no changes needed
    assert (tmp_path / "nochange.inp").read_text() == "*Step\n*Static\n"


def _make_frd_buffer(node_ids_coords, elem_records):
    """Build a minimal binary FRD buffer for testing.

    node_ids_coords: list of (id, x, y, z)
    elem_records: list of (eid, nid, mat, [node_id, ...])
    """
    node_dt = np.dtype([("i", "i4"), ("x", "f8"), ("y", "f8"), ("z", "f8")])
    node_arr = np.array(node_ids_coords, dtype=node_dt)
    elem_ints = []
    for eid, nid, mat, nids in elem_records:
        elem_ints.extend([eid, nid, 0, mat] + list(nids))
    elem_arr = np.array(elem_ints, dtype="i4")
    return (
        b"    2C  3\n"
        + node_arr.tobytes()
        + b"    3C  \n"
        + elem_arr.tobytes()
        + b"    1PSTEP\n"
    )


@pytest.mark.parametrize(
    "elem_type,node_count,elem_nodes",
    [
        ("tetra", 4, [1, 2, 3, 4]),  # nid=3
        ("triangle", 3, [1, 2, 3]),  # nid=7
        ("wedge", 6, [1, 2, 3, 4, 5, 6]),  # nid=2
        ("qwedge", 15, list(range(1, 16))),  # nid=5
    ],
)
def test_new_element_types(tmp_path, elem_type, node_count, elem_nodes):
    """Tetra, wedge, and quadratic-wedge elements convert without error."""
    nid_map = {"tetra": 3, "triangle": 7, "wedge": 2, "qwedge": 5}
    nid = nid_map[elem_type]
    coords = [(i + 1, float(i), float(i % 3), float(i % 2)) for i in range(node_count)]
    buf = _make_frd_buffer(coords, [(1, nid, 1, elem_nodes)])
    frd_path = tmp_path / f"{elem_type}.frd"
    frd_path.write_bytes(buf)
    result = frd2vtu.frdbin2vtu(str(frd_path), str(tmp_path))
    assert result is not None, f"{elem_type}: conversion returned None"
    assert result.n_cells == 1, f"{elem_type}: expected 1 cell"
    assert result.n_points == node_count, f"{elem_type}: expected {node_count} points"

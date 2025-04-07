#!/usr/bin/env python
"""
Pytest tests for frd2vtu conversion functionality.
Tests a variety of FRD files with different characteristics.
"""

import os
import pytest
from pathlib import Path
import frd2vtu
import frd2vtu.basic_plot
import pyvista as pv

# Get the test/frds directory
TEST_DIR = Path(__file__).parent / "frds"


@pytest.fixture
def test_files():
    """Fixture providing test FRD files with different characteristics."""
    return {
        "small": [
            "simplebeam.frd",
            "truss.frd",
            "oneel.frd",
        ],
        "medium": [
            "shell7.frd",
            "contact11.frd",
            "planestress3.frd",
        ],
        "large": [
            "thermomech.frd",
            "concretebeam.frd",
            "contact19.frd",
        ],
        "special": [
            # "zerocoeff.frd",  # Very small file
            "segmentunsmooth.frd",  # Complex geometry
            "induction.frd",  # Large file with different element types
        ],
    }


def test_frd_file_exists(test_files):
    """Test that all test files exist."""
    for category in test_files.values():
        for file in category:
            assert (TEST_DIR / file).exists(), f"Test file not found: {file}"


@pytest.mark.parametrize("category", ["small", "medium", "large", "special"])
def test_frd_conversion(test_files, category):
    """Test FRD to VTU conversion for files in each category."""
    for file in test_files[category]:
        frd_path = TEST_DIR / file
        result = frd2vtu.frdbin2vtu(str(frd_path))
        assert result is not None, f"Failed to convert {file}"
        assert isinstance(result, pv.UnstructuredGrid), (
            f"Result for {file} is not a PyVista grid"
        )


def test_vtu_output(test_files):
    """Test that VTU files are created and valid."""
    for category in test_files.values():
        for file in category:
            frd_path = TEST_DIR / file
            vtu_path = frd_path.with_suffix(".vtu")

            # Convert the file
            result = frd2vtu.frdbin2vtu(str(frd_path))
            assert result is not None, f"Failed to convert {file}"

            # Check that VTU file was created
            assert vtu_path.exists(), f"VTU file not created for {file}"

            # Try to read the VTU file
            try:
                grid = pv.read(vtu_path)
                assert isinstance(grid, pv.UnstructuredGrid), (
                    f"Invalid VTU file for {file}"
                )
            except Exception as e:
                pytest.fail(f"Failed to read VTU file for {file}: {str(e)}")


def test_grid_properties(test_files):
    """Test that converted grids have expected properties."""
    for category in test_files.values():
        for file in category:
            frd_path = TEST_DIR / file
            result = frd2vtu.frdbin2vtu(str(frd_path))
            assert result is not None, f"Failed to convert {file}"

            # Check basic grid properties
            assert result.n_points > 0, f"Grid for {file} has no points"
            assert result.n_cells > 0, f"Grid for {file} has no cells"

            # Check that expected data arrays are present
            assert "ccx_id" in result.point_data, (
                f"Missing ccx_id in point data for {file}"
            )
            assert "ccx_id" in result.cell_data, (
                f"Missing ccx_id in cell data for {file}"
            )
            assert "ccx_mat" in result.cell_data, (
                f"Missing ccx_mat in cell data for {file}"
            )


@pytest.mark.parametrize("file", ["simplebeam.frd"])
def test_specific_files(file):
    """Test specific files that might have special characteristics."""
    frd_path = TEST_DIR / file
    result = frd2vtu.frdbin2vtu(str(frd_path))
    assert result is not None, f"Failed to convert {file}"

    # Additional specific checks can be added here based on known characteristics
    # of these files


def test_basic_plot(tmp_path, test_files):
    """Test that the basic_plot function generates PNG files from VTU files."""
    # Use a small test file for plotting
    frd_file = "simplebeam.frd"
    frd_path = TEST_DIR / frd_file
    vtu_path = tmp_path / frd_path.with_suffix(".vtu").name

    # Convert FRD to VTU
    result = frd2vtu.frdbin2vtu(str(frd_path))
    assert result is not None, f"Failed to convert {frd_file}"
    result.save(str(vtu_path))

    # Run the plotter
    frd2vtu.basic_plot.basic_plots([str(vtu_path)], parallel=False)

    # Check that the PNG file was created
    png_path = vtu_path.with_suffix(".png")
    assert png_path.exists(), f"PNG file not created for {vtu_path}"

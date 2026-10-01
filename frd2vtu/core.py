#!/usr/bin/env python
"""
Core conversion functionality for FRD to VTU.
"""

import logging
import multiprocessing
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import pyvista as pv
import vtk

logger = logging.getLogger(__name__)

NodeMapper = Callable[[np.ndarray, np.ndarray], np.ndarray]


@dataclass(frozen=True)
class ElementSpec:
    vtk_type: int
    n_nodes: int
    map_nodes: NodeMapper

    @property
    def stride(self) -> int:
        return 4 + self.n_nodes


def _linear_nodes(n: int) -> NodeMapper:
    def map_nodes(e: np.ndarray, nz: np.ndarray) -> np.ndarray:
        return nz[e[..., :n]]

    return map_nodes


def _quad_hex_nodes(e: np.ndarray, nz: np.ndarray) -> np.ndarray:
    return nz[np.concatenate((e[..., :12], e[..., 16:], e[..., 12:16]), axis=-1)]


# CalculiX element type id -> VTK cell type and node connectivity
ELEMENT_SPECS: Dict[int, ElementSpec] = {
    1: ElementSpec(vtk.VTK_HEXAHEDRON, 8, _linear_nodes(8)),
    2: ElementSpec(vtk.VTK_WEDGE, 6, _linear_nodes(6)),
    3: ElementSpec(vtk.VTK_TETRA, 4, _linear_nodes(4)),
    4: ElementSpec(vtk.VTK_QUADRATIC_HEXAHEDRON, 20, _quad_hex_nodes),
    5: ElementSpec(vtk.VTK_QUADRATIC_WEDGE, 15, _linear_nodes(15)),
    6: ElementSpec(vtk.VTK_QUADRATIC_TETRA, 10, _linear_nodes(10)),
    7: ElementSpec(vtk.VTK_TRIANGLE, 3, _linear_nodes(3)),
    8: ElementSpec(vtk.VTK_QUADRATIC_TRIANGLE, 6, _linear_nodes(6)),
    9: ElementSpec(vtk.VTK_QUAD, 4, _linear_nodes(4)),
    10: ElementSpec(vtk.VTK_QUADRATIC_QUAD, 8, _linear_nodes(8)),
    11: ElementSpec(vtk.VTK_LINE, 2, _linear_nodes(2)),
    12: ElementSpec(vtk.VTK_QUADRATIC_EDGE, 3, _linear_nodes(3)),
}

# Kept for tests and external reference
e2nn: Dict[int, int] = {nid: spec.n_nodes for nid, spec in ELEMENT_SPECS.items()}


def split_blocks(buf: bytes) -> Optional[List[List[Tuple[int, int, bytes]]]]:
    """
    Split the binary buffer into blocks based on specific patterns.

    Per-pattern regex scans are kept rather than a single alternation: on
    CPython the literal-prefix optimisation makes 7 simple scans several times
    faster than one alternation (measured ~40-70x), even though it reads the
    buffer more than once.

    Args:
        buf: Binary buffer containing the .frd file content

    Returns:
        List of lists containing tuples of (start, end, pattern) for each block,
        or None if the format is not binary
    """
    patterns = [
        b"    2C  (.*?)3\n",
        b"    3C  (.*?)\n",
        b"    1PSTEP(.*?)\n",
        b"1ALL\n",
        b"3    1\n",
        b"0    0\n",
        b" 9999",
    ]
    out = [
        [(m.start(), m.end(), m[0]) for m in re.finditer(pattern, buf)]
        for pattern in patterns
    ]
    if out[0] == []:
        logger.info("frd format not binary")
        return None
    return out


def is_binary_frd(buf: bytes) -> bool:
    """True if the buffer contains a binary CalculiX node block (2C)."""
    return split_blocks(buf) is not None


def _element_block_end(lcs: List[List[Tuple[int, int, bytes]]], buf_len: int) -> int:
    """End offset of the element connectivity block (before 1PSTEP if present)."""
    return lcs[2][0][0] if lcs[2] else buf_len


def _parse_elements(
    elm: np.ndarray, nz: np.ndarray
) -> Tuple[Dict[int, np.ndarray], np.ndarray, np.ndarray]:
    """
    Decode the element connectivity block.

    Element records are variable length (stride depends on type), so a cheap
    sequential pass records the start offset and type of each element; the node
    connectivity is then gathered per type with a single fancy-index. `eid` and
    `emat` are ordered to match the PyVista cell order (types grouped in
    first-seen order), so `cell_data["ccx_id"/"ccx_mat"]` line up with cells even
    for meshes containing more than one element type.
    """
    starts: List[int] = []
    types: List[int] = []
    nn = 0
    while nn < len(elm):
        nid = int(elm[1 + nn])
        spec = ELEMENT_SPECS.get(nid)
        if spec is None:
            logger.info("Unknown element type: %s", nid)
            break
        starts.append(nn)
        types.append(nid)
        nn += spec.stride

    if not starts:
        return {}, np.array([], dtype=np.intp), np.array([], dtype=np.intp)

    starts_arr = np.asarray(starts, dtype=np.intp)
    types_arr = np.asarray(types)

    els: Dict[int, np.ndarray] = {}
    eid_parts: List[np.ndarray] = []
    emat_parts: List[np.ndarray] = []
    for nid in dict.fromkeys(types):
        spec = ELEMENT_SPECS[nid]
        s = starts_arr[types_arr == nid]
        cols = s[:, None] + np.arange(4, 4 + spec.n_nodes)
        els[spec.vtk_type] = spec.map_nodes(elm[cols], nz)
        eid_parts.append(elm[s])
        emat_parts.append(elm[s + 3])

    eid = np.concatenate(eid_parts).astype(np.intp)
    emat = np.concatenate(emat_parts).astype(np.intp)
    return els, eid, emat


def frdbin2vtu(
    file_path: str, output_dir: Optional[str] = None
) -> Optional[pv.UnstructuredGrid]:
    """
    Convert a single binary .frd file to .vtu format.

    Args:
        file_path: Path to the input .frd file
        output_dir: Optional directory to save the output .vtu file

    Returns:
        PyVista UnstructuredGrid object if successful, None otherwise
    """
    starttime = time.time()
    path = Path(file_path)
    logger.info("Converting %s", file_path)
    try:
        buf = path.read_bytes()
    except OSError as e:
        logger.info("Error reading file %s: %s", file_path, e)
        return None
    lcs = split_blocks(buf)
    if lcs is None:
        return None
    nodes = pd.DataFrame(
        np.frombuffer(
            buf[lcs[0][0][1] : lcs[1][0][0]],
            dtype=np.dtype([("i", "i4"), ("x", "f8"), ("y", "f8"), ("z", "f8")]),
        )
    )
    elm_end = _element_block_end(lcs, len(buf))
    elm = np.frombuffer(buf[lcs[1][0][1] : elm_end], dtype=np.dtype("i4"))
    nz = np.zeros(nodes["i"].max() + 1, dtype=int)
    nz[nodes["i"]] = np.arange(len(nodes))
    els, eid, emat = _parse_elements(elm, nz)
    ogrid = pv.UnstructuredGrid(els, nodes[["x", "y", "z"]].values)
    ogrid.cell_data["ccx_id"] = eid
    ogrid.cell_data["ccx_mat"] = emat
    ogrid.point_data["ccx_id"] = nodes["i"]
    if not lcs[2]:
        output_path = (
            Path(output_dir) / path.name.replace(".frd", ".vtu")
            if output_dir
            else path.with_suffix(".vtu")
        )
        ogrid.save(str(output_path))
        logger.info("Saved %s", output_path)
        logger.info("Elapsed time: %.3f seconds", time.time() - starttime)
        return ogrid

    endblocks = lcs[3] + lcs[4] + lcs[5]
    endblocks.sort(key=lambda x: x[0])
    headers = [buf[j[0][0] : j[1][1]] for j in zip(lcs[2], endblocks)]
    for n, bl in enumerate(headers):
        lns = bl.decode("ascii").split("\n")
        if bl.find(b"MODAL") != -1 and bl.find(b"DISP") != -1:
            lns = lns[5:]

        # on some platforms the timestamp gets formatted without space from the run type identifier, causing split to fail.
        # now relies on timestamp starting from 12th character
        timestamp, nn = lns[1][12:].split()[:2]
        timestamp, nn = float(timestamp), int(nn)
        name = lns[2].split()[1]
        if name in ["NORM", "SENMISE", "SENPS1", "SDV"]:
            continue
        ncomp = int(lns[2].split()[2])
        arrn = f"{name}_{timestamp:.3f}"
        logger.info("timestamp: %.3f, nn: %s, array: %s", timestamp, nn, arrn)

        # set the start of the binary block to the end of the ascii block
        startblock = endblocks[n][1]
        ncl = {6: 6, 4: 3, 1: 1, 20: 20}
        nms = [("c_" + str(i), "f4") for i in range(ncl[ncomp])]
        dt = np.dtype([("id", "i4")] + nms)
        endblock = dt.itemsize * int(nn) + startblock
        na = pd.DataFrame(np.frombuffer(buf[startblock:endblock], dtype=dt))
        if len(na) != len(nodes):
            missing_values = nodes[~nodes["i"].isin(na["id"])]["i"]
            padding = pd.DataFrame({"id": missing_values})
            for col in na.columns:
                if col != "id":
                    padding[col] = 0
            na = pd.concat([na, padding], ignore_index=True)
        ogrid.point_data[arrn] = na[[i[0] for i in nms]].values
    output_path = (
        Path(output_dir) / path.name.replace(".frd", ".vtu")
        if output_dir
        else path.with_suffix(".vtu")
    )
    ogrid.save(str(output_path))
    logger.info("Saved %s", output_path)
    logger.info("Elapsed time: %.3f seconds", time.time() - starttime)
    return ogrid


def _convert_one(args: Tuple[str, Optional[str]]) -> None:
    """Pool worker: convert a single file, discarding the returned grid.

    Returning the grid would pickle the whole mesh back to the parent; the
    worker only needs the side effect of writing the .vtu.
    """
    frdbin2vtu(*args)


def frd2vtu(
    frd_files: List[str], parallel: bool = True, output_dir: Optional[str] = None
) -> None:
    """
    Convert one or more .frd files to .vtu format.

    Args:
        frd_files: List of paths to .frd files to convert
        parallel: Whether to use parallel processing (default: True)
        output_dir: Optional directory to save output .vtu files
    """
    if not frd_files:
        logger.info("No input files specified")
        return
    if parallel:
        with multiprocessing.Pool() as p:
            for _ in p.imap_unordered(
                _convert_one, [(f, output_dir) for f in frd_files]
            ):
                pass
    else:
        for f in frd_files:
            frdbin2vtu(f, output_dir)


def prepare_inp_for_binary(
    inp_files: List[str], output_dir: Optional[str] = None
) -> None:
    """
    Prepare CalculiX input files for binary output.

    Args:
        inp_files: List of paths to .inp files to modify
        output_dir: Optional directory to save modified files
    """
    for fl in inp_files:
        path = Path(fl)
        lns = path.read_text().splitlines(keepends=True)
        output = False
        for i, ln in enumerate(lns):
            lw = ln.lower()
            if lw.startswith("*el file"):
                lns[i] = lw.replace("*el file", "*element output")
                output = True
            if lw.startswith("*node file"):
                lns[i] = lw.replace("*node file", "*node output")
                output = True
        if output:
            out_path = Path(output_dir) / path.name if output_dir else path.name
            logger.info("Read %s, writing for binary output to %s", fl, out_path)
            Path(out_path).write_text("".join(lns))
        else:
            logger.info("No changes needed for %s", fl)

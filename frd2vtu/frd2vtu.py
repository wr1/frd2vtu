#!/usr/bin/env python
import numpy as np
import re
import pyvista as pv
import vtk
import fire
import time
import pandas as pd
import multiprocessing


e2nn = {
    1: 8,
    2: 6,
    3: 4,
    5: 15,
    6: 10,
    4: 20,
    7: 3,
    8: 6,
    9: 4,
    10: 8,
    12: 3,
    11: 2,
}


def split_blocks(buf):
    patterns = [
        b"    2C(.*?)3\n",
        b"    3C(.*?)\n",
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
        print(f"frd format not binary")
        return None

    return out


def frdbin2vtu(file_path):
    starttime = time.time()
    print(f"Converting {file_path}")
    buf = open(file_path, "rb").read()
    lcs = split_blocks(buf)
    if lcs is None:
        return None

    nodes = pd.DataFrame(
        np.frombuffer(
            buf[lcs[0][0][1] : lcs[1][0][0]],
            dtype=np.dtype([("i", "i4"), ("x", "f8"), ("y", "f8"), ("z", "f8")]),
        )
    )

    elm = np.frombuffer(
        buf[lcs[1][0][1] : lcs[2][0][0]],
        dtype=np.dtype("i4"),
    )
    nz = np.zeros(nodes["i"].max() + 1, dtype=int)

    nz[nodes["i"]] = np.arange(len(nodes))

    els, nn = {}, 0
    eid, emat = [], []
    while True:
        if nn >= len(elm):
            break

        nid = elm[1 + nn]
        ni = e2nn[nid]
        elmarr = elm[0 + nn : ni + 4 + nn]
        eid.append(elmarr[0])
        emat.append(elmarr[3])
        # deal with 20 node hexahedron
        if nid == 4:
            if vtk.VTK_QUADRATIC_HEXAHEDRON not in els:
                els[vtk.VTK_QUADRATIC_HEXAHEDRON] = []
            e = elmarr[4:].tolist()
            els[vtk.VTK_QUADRATIC_HEXAHEDRON].append(nz[e[:12] + e[16:] + e[12:16]])
            nn += 24
        elif nid == 1:
            if vtk.VTK_HEXAHEDRON not in els:
                els[vtk.VTK_HEXAHEDRON] = []
            e = elmarr[4:].tolist()
            els[vtk.VTK_HEXAHEDRON].append(nz[e[:8]])
            nn += 12
        elif nid == 11:
            if vtk.VTK_LINE not in els:
                els[vtk.VTK_LINE] = []
            e = elmarr[4:].tolist()
            els[vtk.VTK_LINE].append(nz[e[:2]])
            nn += 6
        elif nid == 12:
            if vtk.VTK_QUADRATIC_EDGE not in els:
                els[vtk.VTK_QUADRATIC_EDGE] = []
            e = elmarr[4:].tolist()
            els[vtk.VTK_QUADRATIC_EDGE].append(nz[e[:3]])
            nn += 7
        elif nid == 10:
            if vtk.VTK_QUADRATIC_QUAD not in els:
                els[vtk.VTK_QUADRATIC_QUAD] = []
            e = elmarr[4:].tolist()
            els[vtk.VTK_QUADRATIC_QUAD].append(nz[e[:8]])
            nn += 12
        elif nid == 6:
            if vtk.VTK_QUADRATIC_TETRA not in els:
                els[vtk.VTK_QUADRATIC_TETRA] = []
            e = elmarr[4:].tolist()
            els[vtk.VTK_QUADRATIC_TETRA].append(nz[e[:10]])
            nn += 14
        elif nid == 9:
            if vtk.VTK_QUAD not in els:
                els[vtk.VTK_QUAD] = []
            e = elmarr[4:].tolist()
            els[vtk.VTK_QUAD].append(nz[e[:4]])
            nn += 8
        else:
            print(f"Unknown element type: {nid}")
            break

    # convert list of lists to numpy arrays
    for i in els:
        els[i] = np.array(els[i])

    ogrid = pv.UnstructuredGrid(els, nodes[["x", "y", "z"]].values)

    ogrid.cell_data["ccx_id"] = np.array(eid)
    ogrid.cell_data["ccx_mat"] = np.array(emat)
    ogrid.point_data["ccx_id"] = nodes["i"]

    # join the diffent types of endings for ascii blocks
    endblocks = lcs[3] + lcs[4] + lcs[5]

    endblocks.sort(key=lambda x: x[0])

    headers = [buf[j[0][0] : j[1][1]] for j in zip(lcs[2], endblocks)]

    for n, bl in enumerate(headers):
        lns = bl.decode("ascii").split("\n")

        if bl.find(b"MODAL") != -1 and bl.find(b"DISP") != -1:
            # fix for modal analysis
            lns = lns[5:]

        # on some platforms the timestamp gets formatted without space from the run type identifier, causing split to fail.
        # now relies on timestamp starting from 12th character
        timestamp, nn = lns[1][12:].split()[:2]
        timestamp, nn = float(timestamp), int(nn)
        name = lns[2].split()[1]

        if name in ["NORM", "SENMISE", "SENPS1", "SDV"]:
            continue

        ncomp = int(lns[2].split()[2])
        print(f"timestamp: {timestamp:.3f}, nn: {nn}, name: {name}")

        # set the start of the binary block to the end of the ascii block
        startblock = endblocks[n][1]

        ncl = {6: 6, 4: 3, 1: 1, 20: 20}

        nms = [("c_" + str(i), "f4") for i in range(ncl[ncomp])]
        dt = np.dtype([("id", "i4")] + nms)

        endblock = dt.itemsize * int(nn) + startblock

        na = pd.DataFrame(np.frombuffer(buf[startblock:endblock], dtype=dt))

        # padding missing values for nodes that are not connected to elements
        if len(na) != len(nodes):
            missing_values = nodes[~nodes["i"].isin(na["id"])]["i"]
            padding = pd.DataFrame({"id": missing_values})
            for col in na.columns:
                if col != "id":
                    padding[col] = 0

            na = pd.concat([na, padding], ignore_index=True)

        arrn = f"{name}_{timestamp:.3f}"
        ogrid.point_data[arrn] = na[[i[0] for i in nms]].values

    of = file_path.replace(".frd", ".vtu")
    ogrid.save(of)
    print(f"Saved {of}")
    endtime = time.time()
    print(f"Elapsed time: {endtime - starttime} seconds")
    return ogrid


def frd2vtu(*frd):
    parr = True
    if parr:
        p = multiprocessing.Pool()
        p.map(frdbin2vtu, frd)
        p.close()
        # p.join()
    else:
        for f in frd:
            frdbin2vtu(f)


def main():
    fire.Fire(frd2vtu)


if __name__ == "__main__":
    main()

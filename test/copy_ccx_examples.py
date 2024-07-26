#! /usr/bin/env python

import fire
import os


def frdasc2bin(fl):
    lns = open(fl).readlines()
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
        with open(os.path.basename(fl), "w") as f:
            f.writelines(lns)


def copy_file_to_dir(*src, dest="."):
    runscript = ""
    for f in src:
        frdasc2bin(f)
        runscript += f"ccx -i {os.path.basename(f).split('.')[0]} \n"

    with open("runscript.sh", "w") as f:
        f.write(runscript)


def main():
    fire.Fire(copy_file_to_dir)


if __name__ == "__main__":
    main()

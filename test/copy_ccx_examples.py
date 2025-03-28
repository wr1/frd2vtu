#! /usr/bin/env python

import fire
import os

def frdasc2bin(fl):
    """
    Convert an ASCII .frd file configuration to binary output format.

    This function modifies CalculiX input file lines to request binary output
    instead of ASCII, which is necessary for compatibility with frd2vtu.

    Args:
        fl (str): Path to the input file to modify.

    Returns:
        None: Writes the modified content to a file with the same basename in the current directory.
    """
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
        print(f"Read {fl}, writing for binary output to {os.path.basename(fl)}")
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
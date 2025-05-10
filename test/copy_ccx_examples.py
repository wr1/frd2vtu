#! /usr/bin/env python

import argparse
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

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
        logger.info(f"Read {fl}, writing for binary output to {os.path.basename(fl)}")
        with open(os.path.basename(fl), "w") as f:
            f.writelines(lns)

def copy_file_to_dir(src_files: List[str], dest: str = "."):
    """Copy and process files to the destination directory."""
    runscript = ""
    for f in src_files:
        frdasc2bin(f)
        runscript += f"ccx -i {os.path.basename(f).split('.')[0]} \n"
    with open("runscript.sh", "w") as f:
        f.write(runscript)

def main():
    """Entry point for the command-line interface using argparse."""
    parser = argparse.ArgumentParser(
        description="Convert ASCII .frd configurations to binary and generate a run script."
    )
    parser.add_argument(
        "src_files",
        nargs="+",
        help="Source files to process"
    )
    parser.add_argument(
        "--dest",
        default=".",
        help="Destination directory (default: current directory)"
    )
    args = parser.parse_args()
    copy_file_to_dir(args.src_files, dest=args.dest)

if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
CLI for FRD to VTU conversion.
"""

from treeparse import cli, command, option, argument
from .core import frd2vtu, prepare_inp_for_binary
from typing import List
from pathlib import Path


def convert(frd_files: List[str], no_parallel: bool = False, output_dir: str = None):
    """Convert CalculiX .frd files to VTK .vtu files."""
    if not output_dir and frd_files:
        output_dir = str(Path(frd_files[0]).parent)
    parallel = not no_parallel
    frd2vtu(frd_files, parallel=parallel, output_dir=output_dir)


def iprep(inp_files: List[str], output_dir: str = None):
    """Prepare CalculiX .inp files for binary output."""
    if not output_dir and inp_files:
        output_dir = str(Path(inp_files[0]).parent)
    prepare_inp_for_binary(inp_files, output_dir=output_dir)


app = cli(
    name="frd2vtu",
    help="Convert CalculiX .frd files to VTK .vtu files.",
    commands=[
        command(
            name="convert",
            help="Convert .frd files to .vtu",
            callback=convert,
            arguments=[
                argument(name="frd_files", nargs="*", arg_type=str, help=".frd files to convert"),
            ],
            options=[
                option(flags=["--no-parallel", "-n"], arg_type=bool, default=False, is_flag=True, help="Disable parallel processing"),
                option(flags=["--output-dir", "-o"], arg_type=str, help="Output directory for .vtu files"),
            ],
        ),
        command(
            name="iprep",
            help="Prepare .inp files for binary output",
            callback=iprep,
            arguments=[
                argument(name="inp_files", nargs="*", arg_type=str, help=".inp files to prepare"),
            ],
            options=[
                option(flags=["--output-dir", "-o"], arg_type=str, help="Output directory for modified .inp files"),
            ],
        ),
    ],
)


def main():
    app.run()


if __name__ == "__main__":
    main()

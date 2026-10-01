"""Prepare CalculiX .inp files for binary FRD output and write runscript.sh."""

import logging
from pathlib import Path

from treeparse import argument, cli, option

from frd2vtu._logging import configure_logging

logger = logging.getLogger(__name__)


def frdasc2bin(fl: str) -> None:
    """Rewrite *node file / *el file to binary output keywords."""
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
        out = path.name
        logger.info("Read %s, writing for binary output to %s", fl, out)
        Path(out).write_text("".join(lns))


def copy_file_to_dir(src_files: list[str], dest: str = ".") -> None:
    """Convert inputs and write a CalculiX runscript.sh in dest."""
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)
    runscript = ""
    for f in src_files:
        frdasc2bin(f)
        stem = Path(f).stem
        runscript += f"ccx -i {stem}\n"
    (dest_path / "runscript.sh").write_text(runscript)


def copy_examples(src_files: list[str], dest: str = ".") -> None:
    copy_file_to_dir(src_files, dest=dest)


app = cli(
    name="copy_ccx_examples",
    help="Prepare CalculiX .inp files for binary FRD output and write runscript.sh.",
    callback=copy_examples,
    arguments=[
        argument(
            name="src_files",
            nargs="*",
            arg_type=str,
            help="CalculiX .inp files",
        ),
    ],
    options=[
        option(
            flags=["--dest", "-d"],
            arg_type=str,
            default=".",
            help="Directory for runscript.sh (default: .)",
        ),
    ],
)


def main() -> None:
    configure_logging()
    app.run()


if __name__ == "__main__":
    main()

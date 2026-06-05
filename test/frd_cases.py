"""Shared FRD corpus list (binary mesh files only)."""

from pathlib import Path

from frd2vtu.core import is_binary_frd

FRDS_DIR = Path(__file__).parent / "frds"
FRD_FILES: list[str] = sorted(
    p.name for p in FRDS_DIR.glob("*.frd") if is_binary_frd(p.read_bytes())
)

# ASCII header-only stubs kept in test/frds/ but not parametrized
SKIPPED_FRDS: frozenset[str] = frozenset(
    p.name for p in FRDS_DIR.glob("*.frd") if p.name not in FRD_FILES
)


def frd_params():
    for name in FRD_FILES:
        yield name

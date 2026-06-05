"""Make test helpers (e.g. frd_cases) importable from test modules."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

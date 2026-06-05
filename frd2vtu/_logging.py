"""CLI logging setup (not configured on library import)."""

import logging


def configure_logging(level: int = logging.INFO) -> None:
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level, format="%(message)s")

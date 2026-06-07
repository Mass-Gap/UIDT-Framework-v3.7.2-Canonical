"""Runtime capability checks for the PR-0.5 dashboard."""

from __future__ import annotations

import importlib.util


def has_textual() -> bool:
    """Return True when the Textual package can be imported."""
    return importlib.util.find_spec("textual") is not None


"""
AG-Sim — Blind Simulation Engine (PREREG-PR-B1)
================================================
This sub-package implements the stochastic matrix-model simulation for the
preregistered blinded partition-selection protocol.

BLINDING CONTRACT:
    This package outputs ONLY raw spectrum arrays.  It contains ZERO partition
    detection, clustering, comparison, or scoring logic.  All forbidden
    patterns listed in config.FORBIDDEN_PATTERNS are mechanically excluded.

IEEE-754 float64 arithmetic throughout.  No mpmath.  No mp.dps = 80.
"""

from __future__ import annotations

__all__ = [
    "action",
    "hmc",
    "metropolis",
    "observables",
    "thermalization",
    "seeds",
    "runner",
]

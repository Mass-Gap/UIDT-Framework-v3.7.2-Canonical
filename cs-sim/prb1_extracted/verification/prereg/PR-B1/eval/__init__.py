"""
AG-Eval — Blind Evaluation Engine for PREREG-PR-B1
====================================================
Spawned ONLY after the data-freeze tag exists.
No shared state with AG-Sim.

Public API:
    detector   — KDE partition detector (Sec. 4.1)
    scoring    — Exact-arithmetic ratio-class scoring (Sec. 4.2–4.4)
    validation — Detector validation gate (Sec. 4.5)
    null_controls — Null control machinery (Sec. 6)
    outcomes   — Decision rules O1–O5 (Sec. 7)
    report     — CSV/JSON report generation
"""

from __future__ import annotations

__all__ = [
    "detector",
    "scoring",
    "validation",
    "null_controls",
    "outcomes",
    "report",
]

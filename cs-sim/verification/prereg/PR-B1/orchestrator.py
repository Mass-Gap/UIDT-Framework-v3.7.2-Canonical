"""
Master Orchestrator — Antigravity 2.0 Protocol Controller
==========================================================
Implements the three-phase execution of the blinded preregistration protocol:

  Phase 0: Pre-flight checks (blinding CI, PI hash, detector validation gate)
  Phase 1: AG-Sim (blind simulation in frozen lexicographic grid order)
  Phase 2: Data Freeze (SHA-256 manifest + tag)
  Phase 3: AG-Eval (scoring of frozen raw data, spawned ONLY after freeze)

Usage:
    python -m prb1 orchestrate --master AG2 [--pilot] [--skip-validation]

Protocol ID: PREREG-PR-B1-002-AG2
Evidence ceiling: [D] — no outcome authorizes any evidence-class upgrade.
"""

from __future__ import annotations

import json
import logging
import pathlib
import sys
import time
from datetime import datetime, timezone
from typing import Any

from .config import (
    PI_COMMITMENT_HEX,
    PI_COMMITMENT_UTC,
    build_grid,
    build_pilot_grid,
    RAW_DATA_DIR,
    OUT_DATA_DIR,
    MANIFEST_DIR,
)
from .blinding_check import check_blinding
from .manifest import generate_manifest, get_latest_manifest, verify_manifest

logger = logging.getLogger("prb1.orchestrator")


class ProtocolError(Exception):
    """Raised when a binding protocol constraint is violated."""
    pass


class OrchestratorState:
    """Tracks the current state of the orchestrator."""

    def __init__(self) -> None:
        self.phase: str = "INIT"
        self.pilot_mode: bool = False
        self.sim_completed: bool = False
        self.data_frozen: bool = False
        self.eval_completed: bool = False
        self.outcome: str | None = None
        self.start_time: str = datetime.now(timezone.utc).isoformat()
        self.errors: list[str] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol_id": "PREREG-PR-B1-002-AG2",
            "phase": self.phase,
            "pilot_mode": self.pilot_mode,
            "sim_completed": self.sim_completed,
            "data_frozen": self.data_frozen,
            "eval_completed": self.eval_completed,
            "outcome": self.outcome,
            "start_time": self.start_time,
            "errors": self.errors,
        }

    def save(self, path: pathlib.Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)


def _check_pi_commitment() -> None:
    """Verify PI hash commitment exists.

    Q2 decision: STRICT ABORT without hash.
    """
    if not PI_COMMITMENT_HEX or not PI_COMMITMENT_HEX.strip():
        raise ProtocolError(
            "FATAL: PI-COMMITMENT hash missing in config.py. "
            "Cannot start blinded production run. "
            "The PI must insert the SHA-256 commitment hex digest "
            "and the UTC timestamp in config.PI_COMMITMENT_HEX and "
            "config.PI_COMMITMENT_UTC before any production trajectory. "
            "See protocol Sec. 5.4."
        )
    if not PI_COMMITMENT_UTC or not PI_COMMITMENT_UTC.strip():
        raise ProtocolError(
            "FATAL: PI-COMMITMENT timestamp missing in config.py. "
            "config.PI_COMMITMENT_UTC must be set. See protocol Sec. 5.4."
        )
    logger.info(
        "PI commitment verified: %s... (committed %s)",
        PI_COMMITMENT_HEX[:16], PI_COMMITMENT_UTC,
    )


def _check_blinding() -> None:
    """Run the blinding CI scan."""
    logger.info("Running blinding check...")
    passed, violations = check_blinding()
    if not passed:
        raise ProtocolError(
            f"FATAL: Blinding check failed with {len(violations)} violation(s). "
            "Production is blocked. Fix violations and re-run."
        )
    logger.info("Blinding check passed.")


def _run_detector_validation() -> None:
    """Execute the detector validation gate (Sec. 4.5).

    Gate failure → O5 abort. No production.
    """
    logger.info("Running detector validation gate (Sec. 4.5)...")
    try:
        from .eval.validation import run_validation_gate
        passed, report = run_validation_gate()
    except ImportError:
        raise ProtocolError(
            "FATAL: eval.validation module not found. "
            "AG-Eval code must be built before orchestrator can run."
        )

    if not passed:
        raise ProtocolError(
            "FATAL: Detector validation gate FAILED (outcome O5). "
            "Production is aborted. The protocol returns to methods revision "
            "under a new preregistration ID. "
            f"Gate report: {report}"
        )
    logger.info("Detector validation gate passed.")


def _run_simulation(pilot: bool = False) -> None:
    """Execute AG-Sim: blind simulation over the parameter grid.

    In pilot mode (Q1 decision): only M0, N in {16, 24, 32}.
    AG-Eval MUST NOT score pilot data.
    """
    from .sim.runner import run_grid

    grid = build_pilot_grid() if pilot else build_grid()
    mode_label = "PILOT" if pilot else "PRODUCTION"

    logger.info(
        "[AG-Sim] Starting %s run: %d cells × 8 seeds = %d total runs.",
        mode_label, len(grid), len(grid) * 8,
    )

    run_grid(grid, output_dir=RAW_DATA_DIR)

    logger.info("[AG-Sim] %s run completed.", mode_label)


def _freeze_data() -> dict[str, Any]:
    """Execute the data freeze: SHA-256 manifest of all raw files.

    After this point, AG-Sim is permanently halted and AG-Eval may begin.
    """
    logger.info("[DATA FREEZE] Generating SHA-256 manifest...")
    manifest = generate_manifest(raw_dir=RAW_DATA_DIR, manifest_dir=MANIFEST_DIR)
    logger.info(
        "[DATA FREEZE] Manifest generated. Hash: %s. Files: %d.",
        manifest["manifest_hash"][:16], manifest["file_count"],
    )
    return manifest


def _run_evaluation() -> dict[str, Any]:
    """Execute AG-Eval: score frozen raw data.

    Spawned ONLY after data-freeze manifest exists.
    """
    # Verify data freeze
    manifest_path = get_latest_manifest(MANIFEST_DIR)
    if manifest_path is None:
        raise ProtocolError(
            "FATAL: No data-freeze manifest found. "
            "AG-Eval cannot start before data freeze."
        )

    passed, _ = verify_manifest(manifest_path, RAW_DATA_DIR)
    if not passed:
        raise ProtocolError(
            "FATAL: Data-freeze manifest verification failed. "
            "Raw data may have been modified after freeze."
        )

    logger.info("[AG-Eval] Data-freeze verified. Starting evaluation...")

    from .eval.report import run_full_evaluation

    results = run_full_evaluation(
        raw_dir=RAW_DATA_DIR,
        out_dir=OUT_DATA_DIR,
    )

    logger.info("[AG-Eval] Evaluation completed. Outcome: %s", results.get("outcome"))
    return results


def orchestrate(
    pilot: bool = False,
    skip_validation: bool = False,
) -> dict[str, Any]:
    """Main orchestration loop.

    Parameters
    ----------
    pilot : bool
        If True, run pilot phase only (M0, N in {16,24,32}).
        AG-Eval will NOT score pilot data (Q1 decision).
    skip_validation : bool
        If True, skip detector validation gate.
        USE ONLY for development/debugging; never for production.
    """
    state = OrchestratorState()
    state.pilot_mode = pilot
    state_path = OUT_DATA_DIR / "orchestrator_state.json"

    try:
        # ─── Phase 0: Pre-flight ─────────────────────────────────────
        state.phase = "PRE-FLIGHT"
        state.save(state_path)

        if not pilot:
            # PI commitment required for production (not for pilot)
            _check_pi_commitment()

        _check_blinding()

        if not skip_validation:
            _run_detector_validation()
        else:
            logger.warning(
                "SKIPPING detector validation gate (--skip-validation). "
                "This is acceptable for development only."
            )

        # ─── Phase 1: AG-Sim ─────────────────────────────────────────
        state.phase = "AG-SIM"
        state.save(state_path)

        _run_simulation(pilot=pilot)
        state.sim_completed = True

        # ─── Phase 2: Data Freeze ────────────────────────────────────
        state.phase = "DATA-FREEZE"
        state.save(state_path)

        manifest = _freeze_data()
        state.data_frozen = True

        if pilot:
            # Q1 decision: AG-Eval MUST NOT score pilot data
            state.phase = "PILOT-COMPLETE"
            state.save(state_path)
            logger.info(
                "[PILOT] Pilot phase complete. AG-Eval will NOT score pilot data. "
                "Review thermalization reports, acceptance rates, and memory usage. "
                "Then run full production with: "
                "python -m prb1 orchestrate --master AG2"
            )
            return {
                "phase": "PILOT-COMPLETE",
                "manifest": manifest,
                "note": "AG-Eval scoring of pilot data is FORBIDDEN (Q1 decision).",
            }

        # ─── Phase 3: AG-Eval ────────────────────────────────────────
        state.phase = "AG-EVAL"
        state.save(state_path)

        results = _run_evaluation()
        state.eval_completed = True
        state.outcome = results.get("outcome", "UNKNOWN")

        state.phase = "COMPLETE"
        state.save(state_path)

        return results

    except ProtocolError as exc:
        state.phase = "ABORTED"
        state.errors.append(str(exc))
        state.save(state_path)
        logger.error(str(exc))
        raise
    except Exception as exc:
        state.phase = "ERROR"
        state.errors.append(f"Unexpected error: {exc}")
        state.save(state_path)
        logger.exception("Unexpected error during orchestration")
        raise


def main(args: list[str] | None = None) -> None:
    """CLI entry point for the orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(
        description="PREREG-PR-B1 Master Orchestrator (Antigravity 2.0)"
    )
    parser.add_argument(
        "--master", default="AG2",
        help="Orchestrator identity (default: AG2)"
    )
    parser.add_argument(
        "--pilot", action="store_true",
        help="Run pilot phase only (M0, N<=32). AG-Eval will NOT score."
    )
    parser.add_argument(
        "--skip-validation", action="store_true",
        help="Skip detector validation gate (development only)."
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose logging."
    )

    parsed = parser.parse_args(args)

    logging.basicConfig(
        level=logging.DEBUG if parsed.verbose else logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    logger.info(
        "PREREG-PR-B1 Orchestrator starting (master=%s, pilot=%s)",
        parsed.master, parsed.pilot,
    )

    try:
        results = orchestrate(
            pilot=parsed.pilot,
            skip_validation=parsed.skip_validation,
        )
        print(json.dumps(results, indent=2, default=str))
    except ProtocolError as exc:
        print(f"\n{'='*72}", file=sys.stderr)
        print(f"PROTOCOL ERROR: {exc}", file=sys.stderr)
        print(f"{'='*72}", file=sys.stderr)
        sys.exit(1)

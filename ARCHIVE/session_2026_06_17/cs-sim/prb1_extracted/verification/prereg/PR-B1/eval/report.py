"""
AG-Eval Report — CSV/JSON Report Generation (Sec. 9)
=====================================================
Complete results table: every cell, every seed, every flag.
Output formats: CSV + JSON (NO Parquet, per Q3 decision).
Markdown summary with outcome classification.
"""

from __future__ import annotations

import csv
import json
import pathlib
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Optional

from ..config import (
    CANDIDATE_SET_P,
    GridCell,
    OUT_DATA_DIR,
)
from .outcomes import (
    CellResult,
    Outcome,
    OutcomeDecision,
    OUTCOME_DESCRIPTIONS,
)
from .validation import ValidationReport, ValidationResult
from .null_controls import (
    MultiTargetResult,
    HotColdResult,
    ScrambledControlResult,
)


# ── Serialisation helpers ───────────────────────────────────────────────────

def _cell_to_dict(cell: GridCell) -> dict[str, Any]:
    """Convert a GridCell NamedTuple to a JSON-friendly dict."""
    return {
        "model": cell.model,
        "N": cell.N,
        "alpha_tilde": cell.alpha_tilde,
        "mu2": cell.mu2,
        "g2": cell.g2,
    }


def _cell_result_to_row(cr: CellResult) -> dict[str, Any]:
    """Flatten a CellResult into a dict suitable for CSV output."""
    row: dict[str, Any] = {
        "model": cr.cell.model,
        "N": cr.cell.N,
        "alpha_tilde": cr.cell.alpha_tilde,
        "mu2": cr.cell.mu2,
        "g2": cr.cell.g2,
        "modal_class": cr.modal_class,
        "modal_frequency": cr.modal_frequency,
        "flags": ";".join(cr.flags) if cr.flags else "",
    }
    # Add class counts for each candidate
    for label in sorted(CANDIDATE_SET_P.keys()):
        row[f"count_{label}"] = cr.class_counts.get(label, 0)
    row["count_UNCLASSIFIED"] = cr.class_counts.get("UNCLASSIFIED", 0)
    return row


def _validation_result_to_row(vr: ValidationResult) -> dict[str, Any]:
    """Flatten a ValidationResult into a dict suitable for CSV output."""
    return {
        "class_label": vr.class_label,
        "N": vr.N,
        "epsilon": vr.epsilon,
        "n_samples": vr.n_samples,
        "n_correct": vr.n_correct,
        "recovery_rate": vr.recovery_rate,
        "threshold": vr.threshold if vr.threshold is not None else "",
        "passed": (
            str(vr.passed) if vr.passed is not None else "INFORMATIONAL"
        ),
    }


# ── CSV writers ─────────────────────────────────────────────────────────────

def write_cell_results_csv(
    cell_results: list[CellResult],
    path: pathlib.Path,
) -> pathlib.Path:
    """Write the complete cell-level results table as CSV.

    One row per grid cell.  Columns: model, N, alpha_tilde, mu2, g2,
    modal_class, modal_frequency, flags, count_[class] for each class.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    if not cell_results:
        path.write_text("# No cell results\n", encoding="utf-8")
        return path

    rows = [_cell_result_to_row(cr) for cr in cell_results]
    fieldnames = list(rows[0].keys())

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return path


def write_validation_csv(
    validation_report: ValidationReport,
    path: pathlib.Path,
) -> pathlib.Path:
    """Write the validation gate results as CSV.

    One row per (class, N, epsilon) triplet.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    if not validation_report.results:
        path.write_text("# No validation results\n", encoding="utf-8")
        return path

    rows = [_validation_result_to_row(vr) for vr in validation_report.results]
    fieldnames = list(rows[0].keys())

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return path


# ── JSON writer ─────────────────────────────────────────────────────────────

def _build_full_report(
    outcome: OutcomeDecision,
    cell_results: list[CellResult],
    validation_report: ValidationReport,
    multi_target: MultiTargetResult,
    scrambled_controls: list[ScrambledControlResult],
    hot_cold_results: list[HotColdResult],
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Build the complete JSON-serialisable report structure."""
    timestamp = datetime.now(timezone.utc).isoformat()

    report: dict[str, Any] = {
        "meta": {
            "protocol": "PREREG-PR-B1",
            "component": "AG-Eval",
            "timestamp_utc": timestamp,
            "format_version": "1.0",
            **(metadata or {}),
        },
        "outcome": {
            "code": outcome.outcome,
            "description": outcome.description,
            "evidence": outcome.evidence,
        },
        "validation_gate": {
            "passed": validation_report.gate_passed,
            "n_triplets": len(validation_report.results),
            "n_failures": len(validation_report.failures),
            "failures": [
                {
                    "class": f.class_label,
                    "N": f.N,
                    "epsilon": f.epsilon,
                    "recovery": f.recovery_rate,
                    "threshold": f.threshold,
                }
                for f in validation_report.failures
            ],
        },
        "null_controls": {
            "multi_target": {
                "is_non_discriminative": multi_target.is_non_discriminative,
                "offending_classes": multi_target.offending_classes,
            },
            "scrambled_controls": [
                {
                    "cell": _cell_to_dict(sc.cell),
                    "modal_class": sc.modal_class,
                    "modal_frequency": sc.modal_frequency,
                    "is_structured": sc.is_structured,
                }
                for sc in scrambled_controls
            ],
            "hot_cold": {
                "n_total": len(hot_cold_results),
                "n_metastable": sum(
                    1 for hc in hot_cold_results if hc.is_metastable
                ),
                "metastable_cells": [
                    {
                        "cell": _cell_to_dict(hc.cell),
                        "hot_modal": hc.hot_modal,
                        "cold_modal": hc.cold_modal,
                    }
                    for hc in hot_cold_results if hc.is_metastable
                ],
            },
        },
        "cell_results": [
            _cell_result_to_row(cr) for cr in cell_results
        ],
    }

    return report


def write_full_report_json(
    outcome: OutcomeDecision,
    cell_results: list[CellResult],
    validation_report: ValidationReport,
    multi_target: MultiTargetResult,
    scrambled_controls: list[ScrambledControlResult],
    hot_cold_results: list[HotColdResult],
    path: pathlib.Path,
    metadata: Optional[dict[str, Any]] = None,
) -> pathlib.Path:
    """Write the complete evaluation report as JSON.

    Contains: outcome, validation gate, null controls, all cell results.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    report = _build_full_report(
        outcome=outcome,
        cell_results=cell_results,
        validation_report=validation_report,
        multi_target=multi_target,
        scrambled_controls=scrambled_controls,
        hot_cold_results=hot_cold_results,
        metadata=metadata,
    )

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str, ensure_ascii=False)

    return path


# ── Markdown summary ────────────────────────────────────────────────────────

def write_markdown_summary(
    outcome: OutcomeDecision,
    cell_results: list[CellResult],
    validation_report: ValidationReport,
    multi_target: MultiTargetResult,
    hot_cold_results: list[HotColdResult],
    path: pathlib.Path,
) -> pathlib.Path:
    """Write a human-readable Markdown summary of the evaluation.

    Contains: outcome, validation gate status, null control status,
    grid-wide statistics, flag counts.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# AG-Eval — PREREG-PR-B1 Evaluation Summary")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now(timezone.utc).isoformat()}")
    lines.append("")

    # Outcome
    lines.append("## Outcome")
    lines.append("")
    lines.append(f"**{outcome.outcome}:** {outcome.description}")
    lines.append("")
    if outcome.evidence:
        lines.append("### Evidence")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(outcome.evidence, indent=2, default=str))
        lines.append("```")
        lines.append("")

    # Validation gate
    lines.append("## Validation Gate")
    lines.append("")
    gate_status = "✅ PASSED" if validation_report.gate_passed else "❌ FAILED"
    lines.append(f"**Status:** {gate_status}")
    lines.append(f"**Triplets tested:** {len(validation_report.results)}")
    if validation_report.failures:
        lines.append(f"**Failures:** {len(validation_report.failures)}")
        lines.append("")
        lines.append("| Class | N | ε | Recovery | Threshold |")
        lines.append("|-------|---|---|----------|-----------|")
        for f in validation_report.failures:
            lines.append(
                f"| {f.class_label} | {f.N} | {f.epsilon:.2f} | "
                f"{f.recovery_rate:.3f} | {f.threshold} |"
            )
    lines.append("")

    # Null controls
    lines.append("## Null Controls")
    lines.append("")
    lines.append(
        f"**Multi-target:** "
        f"{'NON-DISCRIMINATIVE' if multi_target.is_non_discriminative else 'PASSED'}"
    )
    n_metastable = sum(1 for hc in hot_cold_results if hc.is_metastable)
    lines.append(
        f"**Hot/cold consistency:** {n_metastable} metastable cells "
        f"out of {len(hot_cold_results)}"
    )
    lines.append("")

    # Grid-wide statistics
    if cell_results:
        lines.append("## Grid-Wide Statistics")
        lines.append("")
        lines.append(f"**Total cells evaluated:** {len(cell_results)}")

        # Modal class distribution
        class_dist: dict[str, int] = {}
        for cr in cell_results:
            class_dist[cr.modal_class] = class_dist.get(cr.modal_class, 0) + 1

        lines.append("")
        lines.append("### Modal Class Distribution")
        lines.append("")
        lines.append("| Class | Count | Fraction |")
        lines.append("|-------|-------|----------|")
        for label in sorted(class_dist.keys()):
            count = class_dist[label]
            frac = count / len(cell_results)
            lines.append(f"| {label} | {count} | {frac:.3f} |")

        # Flag counts
        flag_counts: dict[str, int] = {}
        for cr in cell_results:
            for flag in cr.flags:
                flag_counts[flag] = flag_counts.get(flag, 0) + 1

        if flag_counts:
            lines.append("")
            lines.append("### Flags")
            lines.append("")
            lines.append("| Flag | Count |")
            lines.append("|------|-------|")
            for flag in sorted(flag_counts.keys()):
                lines.append(f"| {flag} | {flag_counts[flag]} |")

    lines.append("")
    lines.append("---")
    lines.append("*Report generated by AG-Eval (PREREG-PR-B1 blind evaluation engine).*")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ── Convenience: write all outputs ──────────────────────────────────────────

def write_all_reports(
    outcome: OutcomeDecision,
    cell_results: list[CellResult],
    validation_report: ValidationReport,
    multi_target: MultiTargetResult,
    scrambled_controls: list[ScrambledControlResult],
    hot_cold_results: list[HotColdResult],
    output_dir: Optional[pathlib.Path] = None,
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, pathlib.Path]:
    """Write all report files (CSV + JSON + Markdown) to output_dir.

    Returns dict mapping report name → file path.
    """
    if output_dir is None:
        output_dir = OUT_DATA_DIR

    output_dir.mkdir(parents=True, exist_ok=True)

    paths: dict[str, pathlib.Path] = {}

    # Cell results CSV
    paths["cell_results_csv"] = write_cell_results_csv(
        cell_results, output_dir / "cell_results.csv"
    )

    # Validation CSV
    paths["validation_csv"] = write_validation_csv(
        validation_report, output_dir / "validation_gate.csv"
    )

    # Full JSON report
    paths["full_report_json"] = write_full_report_json(
        outcome=outcome,
        cell_results=cell_results,
        validation_report=validation_report,
        multi_target=multi_target,
        scrambled_controls=scrambled_controls,
        hot_cold_results=hot_cold_results,
        path=output_dir / "evaluation_report.json",
        metadata=metadata,
    )

    # Markdown summary
    paths["summary_md"] = write_markdown_summary(
        outcome=outcome,
        cell_results=cell_results,
        validation_report=validation_report,
        multi_target=multi_target,
        hot_cold_results=hot_cold_results,
        path=output_dir / "evaluation_summary.md",
    )

    return paths


# ── Orchestrator entry point ────────────────────────────────────────────────

def run_full_evaluation(
    raw_dir: pathlib.Path,
    out_dir: Optional[pathlib.Path] = None,
) -> dict[str, Any]:
    """Run the complete AG-Eval pipeline on frozen raw data.

    This is the single entry point called by the orchestrator after
    the data-freeze tag exists.

    Pipeline:
      1. Load all raw .npz + .json files from raw_dir
      2. For each cell × seed: run detector + scorer
      3. Aggregate per-cell modal class
      4. Run null controls (multi-target, hot/cold, scrambled)
      5. Decide outcome (O1–O5)
      6. Write all reports (CSV, JSON, Markdown)

    Parameters
    ----------
    raw_dir : Path
        Directory containing frozen raw simulation data (.npz + .json).
    out_dir : Path or None
        Output directory for reports.  Default: config.OUT_DATA_DIR.

    Returns
    -------
    dict
        Summary including 'outcome', 'outcome_label', 'report_paths'.
    """
    import logging

    import numpy as np

    from ..config import (
        build_grid,
        SEEDS_PER_CELL,
        SCRAMBLED_CONTROL_CELLS,
        RAW_DATA_DIR,
    )
    from .detector import detect_partition
    from .scoring import score_partition
    from .null_controls import (
        check_multi_target,
        check_hot_cold_consistency,
        check_scrambled_controls,
    )
    from .outcomes import CellResult, decide_outcome
    from .validation import run_validation_gate

    logger = logging.getLogger("prb1.eval.report")

    if out_dir is None:
        out_dir = OUT_DATA_DIR

    # --- 0. Validation report (already passed in pre-flight, but record it) ---
    validation_passed, validation_report = run_validation_gate()

    # --- 1. Load raw data index ---
    json_files = sorted(raw_dir.glob("*.json"))
    logger.info("Found %d raw run metadata files.", len(json_files))

    # Group runs by cell
    from collections import defaultdict
    cell_runs: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for jf in json_files:
        import json as _json
        with open(jf, "r", encoding="utf-8") as f:
            meta = _json.load(f)
        cell_key = (
            f"{meta['model']}|{meta['N']}|{meta['alpha_tilde']}"
            f"|{meta['mu2']}|{meta['g2']}"
        )
        npz_path = raw_dir / f"{meta['run_uuid']}.npz"
        meta["_npz_path"] = str(npz_path)
        cell_runs[cell_key].append(meta)

    # --- 2. Per-cell scoring ---
    cell_results: list[CellResult] = []

    for cell_key, runs in sorted(cell_runs.items()):
        parts = cell_key.split("|")
        cell = GridCell(
            model=parts[0],
            N=int(parts[1]),
            alpha_tilde=float(parts[2]),
            mu2=float(parts[3]),
            g2=float(parts[4]),
        )

        class_counts: dict[str, int] = {}
        flags: list[str] = []
        seed_classes: dict[int, str] = {}

        for run_meta in runs:
            npz_path = pathlib.Path(run_meta["_npz_path"])
            if not npz_path.exists():
                logger.warning("Missing .npz for run %s", run_meta["run_uuid"])
                continue

            data = np.load(str(npz_path))
            casimir_spectra = data["casimir_spectra"]

            # Check undersampled flag
            if run_meta.get("undersampled", False):
                if "UNDERSAMPLED" not in flags:
                    flags.append("UNDERSAMPLED")

            # Score each measurement
            for meas_idx in range(casimir_spectra.shape[0]):
                eigs = casimir_spectra[meas_idx]
                partition = detect_partition(eigs)
                result = score_partition(partition)
                label = result.assigned_class if result.assigned_class else "UNCLASSIFIED"
                class_counts[label] = class_counts.get(label, 0) + 1

            seed_idx = run_meta.get("seed_index", -1)
            # Determine modal class for this seed's measurements
            seed_class_counts: dict[str, int] = {}
            for meas_idx in range(casimir_spectra.shape[0]):
                eigs = casimir_spectra[meas_idx]
                partition = detect_partition(eigs)
                result = score_partition(partition)
                lbl = result.assigned_class if result.assigned_class else "UNCLASSIFIED"
                seed_class_counts[lbl] = seed_class_counts.get(lbl, 0) + 1
            if seed_class_counts:
                seed_modal = max(seed_class_counts, key=seed_class_counts.get)
                seed_classes[seed_idx] = seed_modal

        # Modal class for the cell
        if class_counts:
            total = sum(class_counts.values())
            modal_class = max(class_counts, key=class_counts.get)
            modal_frequency = class_counts[modal_class] / total
        else:
            modal_class = "UNCLASSIFIED"
            modal_frequency = 0.0

        cell_results.append(CellResult(
            cell=cell,
            modal_class=modal_class,
            modal_frequency=modal_frequency,
            class_counts=class_counts,
            flags=flags,
            seed_classes=seed_classes,
        ))

    logger.info("Scored %d cells.", len(cell_results))

    # --- 3. Null controls ---
    multi_target = check_multi_target(cell_results)
    hot_cold_results = check_hot_cold_consistency(cell_results)
    scrambled_results = check_scrambled_controls(cell_results)

    # --- 4. Decide outcome ---
    outcome = decide_outcome(
        cell_results=cell_results,
        validation_report=validation_report,
        multi_target=multi_target,
        hot_cold_results=hot_cold_results,
    )

    logger.info("Outcome: %s — %s", outcome.outcome.name, outcome.label)

    # --- 5. Write reports ---
    report_paths = write_all_reports(
        outcome=outcome,
        cell_results=cell_results,
        validation_report=validation_report,
        multi_target=multi_target,
        scrambled_controls=scrambled_results,
        hot_cold_results=hot_cold_results,
        output_dir=out_dir,
    )

    return {
        "outcome": outcome.outcome.name,
        "outcome_label": outcome.label,
        "report_paths": {k: str(v) for k, v in report_paths.items()},
        "n_cells_scored": len(cell_results),
    }

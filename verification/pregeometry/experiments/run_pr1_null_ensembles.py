"""Run PR-1 null-ensemble separation metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from verification.pregeometry.dashboard.schemas import assert_no_forbidden_visualization_text
from verification.pregeometry.null_ensembles import NULL_ENSEMBLE_NAMES, generate_all_ensembles, pr0_invariant_trace
from verification.pregeometry.reports.write_pr1_report import write_pr1_report
from verification.pregeometry.separation_metrics import summarize_ensemble_metrics


PR1_OUTPUT_SCHEMA = "uidt-pregeometry-pr1-null-ensembles-v1"


def main() -> None:
    args = _parse_args()
    result = run_pr1_null_ensembles(
        project_root=Path(args.project_root).resolve(),
        iterations=args.iterations,
        seed=args.seed,
        ensemble_size=args.ensemble_size,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


def run_pr1_null_ensembles(
    *,
    project_root: Path,
    iterations: int,
    seed: int,
    ensemble_size: int,
) -> dict[str, object]:
    if iterations < 0:
        raise ValueError("iterations must be non-negative.")
    if ensemble_size < 0:
        raise ValueError("ensemble_size must be non-negative.")

    reference_trace = pr0_invariant_trace(iterations)
    ensembles = generate_all_ensembles(iterations=iterations, seed=seed, ensemble_size=ensemble_size)
    metric_rows = []
    ensemble_payload: dict[str, Any] = {}
    for index, name in enumerate(NULL_ENSEMBLE_NAMES):
        traces = ensembles[name]
        metric = summarize_ensemble_metrics(
            ensemble_name=name,
            reference_trace=reference_trace,
            candidate_traces=[trace.invariants_by_tick for trace in traces],
            seed=seed + index,
        )
        metric_rows.append(metric.as_jsonable())
        ensemble_payload[name] = [trace.as_jsonable() for trace in traces]

    summary: dict[str, object] = {
        "schema": PR1_OUTPUT_SCHEMA,
        "workspace_boundary": "separate experimental pregeometry workspace",
        "scientific_status": {
            "software_invariants": "[A] only for the executed software path",
            "null_model_separation_metrics": "[D]",
            "physical_interpretation": "[D/E]",
        },
        "parameters": {
            "iterations": iterations,
            "seed": seed,
            "ensemble_size": ensemble_size,
            "ensembles": list(NULL_ENSEMBLE_NAMES),
        },
        "pr0_toy": {
            "trace": [item.as_jsonable() for item in reference_trace],
            "final_invariants": reference_trace[-1].as_jsonable() if reference_trace else {"N": 0, "E": 0, "C": 0, "beta_1": 0},
        },
        "metrics": metric_rows,
        "interpretation_boundary": (
            "Nonzero separation means distinguishability from selected nulls only; "
            "all physical interpretation remains [D/E]."
        ),
    }
    assert_no_forbidden_visualization_text(json.dumps(summary, sort_keys=True))

    output_dir = pr1_output_dir(project_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"pr1_null_ensembles_seed{seed}_iter{iterations}_n{ensemble_size}.json"
    ensure_allowed_pr1_output(output_path, project_root=project_root)
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report_path = write_pr1_report(project_root=project_root, summary=summary)
    result = {
        "summary_json": str(output_path.relative_to(project_root)),
        "report": str(report_path.relative_to(project_root)),
        "final_invariants": summary["pr0_toy"]["final_invariants"],  # type: ignore[index]
        "metric_count": len(metric_rows),
        "claim_status": "[D/E]",
    }
    return result


def pr1_output_dir(project_root: Path) -> Path:
    return Path(project_root).resolve() / "verification" / "data" / "pregeometry" / "pr1"


def ensure_allowed_pr1_output(path: Path, *, project_root: Path) -> None:
    target_path = Path(path).resolve()
    root = Path(project_root).resolve()
    allowed = pr1_output_dir(root).resolve()
    if target_path.parent == root:
        raise AssertionError(f"Refusing PR-1 output at repository root: {target_path}")
    try:
        target_path.relative_to(allowed)
    except ValueError as exc:
        raise AssertionError(f"PR-1 output path is outside allowed output directory: {target_path}") from exc


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run PR-1 null-ensemble separation metrics.")
    parser.add_argument("--iterations", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--ensemble-size", type=int, required=True)
    parser.add_argument("--project-root", default=".")
    return parser.parse_args()


if __name__ == "__main__":
    main()

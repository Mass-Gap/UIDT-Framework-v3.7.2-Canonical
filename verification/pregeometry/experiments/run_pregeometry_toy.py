"""Run the UIDT PR-0 pregeometry vertical slice.

Required reproduction command:
    python -m verification.pregeometry.experiments.run_pregeometry_toy --iterations 8 --seed 39
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Tuple

from verification.pregeometry.growth_rules import apply_pr0_growth_step, grow_pr0, is_directed_acyclic
from verification.pregeometry.leakage_audit import assert_no_leakage, default_generation_paths
from verification.pregeometry.null_models import erdos_renyi_integer_threshold, random_dag_integer_threshold
from verification.pregeometry.observables import compute_graph_invariants
from verification.pregeometry.primitives import RelationalState
from verification.pregeometry.reports.write_pregeometry_report import write_report


PROTECTED_ROOT_OUTPUT_FILENAMES = frozenset(
    {
        "pr0_run.json",
        "pr0_report.md",
        "output.json",
        "report.md",
    }
)


def main() -> None:
    args = _parse_args()
    project_root = Path(args.project_root).resolve()
    result = run_pr0(
        project_root=project_root,
        iterations=args.iterations,
        seed=args.seed,
        null_model=args.null_model,
        telemetry=args.telemetry,
        run_id=args.run_id,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


def run_pr0(
    *,
    project_root: Path,
    iterations: int,
    seed: int,
    null_model: str = "erdos_renyi",
    telemetry: bool = False,
    run_id: str | None = None,
) -> Dict[str, object]:
    if iterations < 0:
        raise ValueError("iterations must be non-negative.")
    if null_model not in {"erdos_renyi", "random_dag"}:
        raise ValueError("null_model must be 'erdos_renyi' or 'random_dag'.")

    scan_paths = default_generation_paths(project_root)
    leakage_result = assert_no_leakage(scan_paths, project_root=project_root)

    telemetry_events = ()
    resolved_run_id = run_id
    if telemetry:
        uidt_state, applied_rules, telemetry_events, resolved_run_id = _grow_pr0_with_telemetry(
            project_root=project_root,
            iterations=iterations,
            seed=seed,
            run_id=run_id,
            leakage_passed=leakage_result.passed,
        )
    else:
        uidt_state, applied_rules = grow_pr0(iterations)
    uidt_invariants = compute_graph_invariants(uidt_state)

    if null_model == "erdos_renyi":
        null_state = erdos_renyi_integer_threshold(uidt_invariants.node_count, seed=seed)
    else:
        null_state = random_dag_integer_threshold(uidt_invariants.node_count, seed=seed)
    null_invariants = compute_graph_invariants(null_state)

    output_dir = project_root / "verification" / "data" / "pregeometry"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"pr0_run_seed{seed}_iter{iterations}.json"
    ensure_not_repository_root_output(output_path, project_root=project_root)

    payload: Dict[str, object] = {
        "schema": "uidt-pregeometry-pr0-run-v1",
        "scientific_status": {
            "software_invariants": "[A] only for the executed code path",
            "physical_interpretation": "[D/E]",
        },
        "parameters": {
            "iterations": iterations,
            "seed": seed,
            "null_model": null_model,
        },
        "leakage_audit": leakage_result.as_jsonable(),
        "uidt_toy": {
            "state": uidt_state.as_jsonable(),
            "invariants": uidt_invariants.as_jsonable(),
            "applied_rules": [metadata.name for metadata in applied_rules],
        },
        "null_model": {
            "name": null_model,
            "state": null_state.as_jsonable(),
            "invariants": null_invariants.as_jsonable(),
        },
        "limitations": [
            "No universe simulation is claimed.",
            "No cosmological model is claimed.",
            "No spacetime derivation is claimed.",
            "No gauge-sector derivation is claimed.",
            "No null-model separation score is implemented in PR-0.",
        ],
    }

    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path = write_report(project_root=project_root, run_json_path=output_path)

    result: Dict[str, object] = {
        "run_json": str(output_path.relative_to(project_root)),
        "report": str(report_path.relative_to(project_root)),
        "leakage_audit_passed": leakage_result.passed,
        "uidt_invariants": uidt_invariants.as_jsonable(),
        "null_invariants": null_invariants.as_jsonable(),
    }
    if telemetry:
        from verification.pregeometry.dashboard.schemas import InvariantBlock
        from verification.pregeometry.dashboard.telemetry import make_summary, write_summary

        if resolved_run_id is None:
            raise AssertionError("Telemetry run id was not resolved.")
        summary = make_summary(
            run_id=resolved_run_id,
            seed=seed,
            iterations=iterations,
            null_model=null_model,
            events=telemetry_events,
            uidt_invariants=InvariantBlock(
                N=uidt_invariants.node_count,
                E=uidt_invariants.edge_count,
                C=uidt_invariants.connected_component_count,
                beta_1=uidt_invariants.beta_1,
            ),
            null_invariants=InvariantBlock(
                N=null_invariants.node_count,
                E=null_invariants.edge_count,
                C=null_invariants.connected_component_count,
                beta_1=null_invariants.beta_1,
            ),
            leakage_passed=leakage_result.passed,
            invariant_passed=is_directed_acyclic(uidt_state),
            run_json=str(output_path.relative_to(project_root)),
            report=str(report_path.relative_to(project_root)),
        )
        summary_path = write_summary(project_root, summary)
        result["telemetry_events"] = str(
            (project_root / "verification" / "data" / "pregeometry" / "runs" / resolved_run_id / "events.jsonl").relative_to(project_root)
        )
        result["telemetry_summary"] = str(summary_path.relative_to(project_root))
    return result


def ensure_not_repository_root_output(path: Path, *, project_root: Path) -> None:
    resolved = path.resolve()
    root = project_root.resolve()
    if resolved.parent == root:
        raise AssertionError(f"Refusing to write output artifact to repository root: {resolved}")
    if resolved.name in PROTECTED_ROOT_OUTPUT_FILENAMES and resolved.parent == root:
        raise AssertionError(f"Refusing protected root output filename: {resolved.name}")
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise AssertionError(f"Output path is outside project root: {resolved}") from exc


def _grow_pr0_with_telemetry(
    *,
    project_root: Path,
    iterations: int,
    seed: int,
    run_id: str | None,
    leakage_passed: bool,
) -> Tuple[RelationalState, tuple[object, ...], tuple[object, ...], str]:
    from verification.pregeometry.dashboard.schemas import InvariantBlock
    from verification.pregeometry.dashboard.telemetry import append_event, make_event, make_run_id

    resolved_run_id = run_id or make_run_id(seed=seed, iterations=iterations)
    state = RelationalState.unmarked()
    metadata = []
    events = []
    for step in range(iterations):
        result = apply_pr0_growth_step(state, step)
        state = result.state
        metadata.append(result.metadata)
        invariants = compute_graph_invariants(state)
        acyclic = is_directed_acyclic(state)
        event = make_event(
            run_id=resolved_run_id,
            tick=step + 1,
            seed=seed,
            rule=result.metadata.name,
            invariants=InvariantBlock(
                N=invariants.node_count,
                E=invariants.edge_count,
                C=invariants.connected_component_count,
                beta_1=invariants.beta_1,
            ),
            acyclic=acyclic,
            leakage_passed=leakage_passed,
            invariant_passed=acyclic,
        )
        append_event(project_root, event)
        events.append(event)
    state.assert_invariants()
    if not is_directed_acyclic(state):
        raise AssertionError("PR-0 telemetry growth schedule produced a directed cycle.")
    return state, tuple(metadata), tuple(events), resolved_run_id


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run UIDT PR-0 pregeometry toy harness.")
    parser.add_argument("--iterations", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--null-model", choices=("erdos_renyi", "random_dag"), default="erdos_renyi")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--telemetry", action="store_true")
    parser.add_argument("--run-id", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    main()

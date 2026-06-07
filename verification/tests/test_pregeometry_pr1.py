from __future__ import annotations

import json
from pathlib import Path

import pytest

from verification.pregeometry.dashboard.renderers import render_dashboard_snapshot
from verification.pregeometry.dashboard.telemetry import read_events, read_summary
from verification.pregeometry.experiments.run_pr1_null_ensembles import ensure_allowed_pr1_output, run_pr1_null_ensembles
from verification.pregeometry.experiments.run_pregeometry_toy import run_pr0
from verification.pregeometry.null_ensembles import generate_all_ensembles, pr0_invariant_trace
from verification.pregeometry.separation_metrics import final_state_l1, summarize_ensemble_metrics, trajectory_l1


def test_pr0_invariants_unchanged_for_pr1_reference_trace() -> None:
    trace = pr0_invariant_trace(8)
    final = trace[-1]
    assert final.as_jsonable() == {"N": 7, "E": 7, "C": 1, "beta_1": 1}


def test_null_ensembles_are_deterministic_for_fixed_seed() -> None:
    first = generate_all_ensembles(iterations=5, seed=39, ensemble_size=4)
    second = generate_all_ensembles(iterations=5, seed=39, ensemble_size=4)
    assert first == second


def test_metrics_are_deterministic_for_fixed_input() -> None:
    reference = pr0_invariant_trace(5)
    ensembles = generate_all_ensembles(iterations=5, seed=39, ensemble_size=4)
    traces = [trace.invariants_by_tick for trace in ensembles["erdos_renyi"]]
    first = summarize_ensemble_metrics(
        ensemble_name="erdos_renyi",
        reference_trace=reference,
        candidate_traces=traces,
        seed=39,
    )
    second = summarize_ensemble_metrics(
        ensemble_name="erdos_renyi",
        reference_trace=reference,
        candidate_traces=traces,
        seed=39,
    )
    assert first == second
    assert final_state_l1(reference[-1], traces[0][-1]) >= 0
    assert trajectory_l1(reference, traces[0]) >= 0


def test_forbidden_labels_are_rejected_by_metric_summary() -> None:
    reference = pr0_invariant_trace(2)
    with pytest.raises(ValueError):
        summarize_ensemble_metrics(
            ensemble_name="Minkowski",
            reference_trace=reference,
            candidate_traces=(reference,),
            seed=39,
        )


def test_pr1_runtime_artifacts_stay_under_allowed_directory(tmp_path: Path) -> None:
    result = run_pr1_null_ensembles(project_root=tmp_path, iterations=4, seed=39, ensemble_size=3)
    summary_rel = Path(str(result["summary_json"]))
    assert summary_rel.parts[:4] == ("verification", "data", "pregeometry", "pr1")
    assert Path(str(result["report"])).parts[:3] == ("verification", "pregeometry", "reports")
    with pytest.raises(AssertionError):
        ensure_allowed_pr1_output(tmp_path / "pr1.json", project_root=tmp_path)


def test_pr1_report_scopes_nonzero_separation_to_selected_nulls(tmp_path: Path) -> None:
    result = run_pr1_null_ensembles(project_root=tmp_path, iterations=4, seed=39, ensemble_size=3)
    report = tmp_path / Path(str(result["report"]))
    text = report.read_text(encoding="utf-8")
    assert "distinguishability from selected null" in text
    assert "Physical interpretation remains outside the scope" in text
    assert "[D/E]" in text


def test_dashboard_remains_read_only_with_pr1_files_present(tmp_path: Path) -> None:
    run_pr0(project_root=tmp_path, iterations=3, seed=39, telemetry=True, run_id="dash_pr1")
    run_pr1_null_ensembles(project_root=tmp_path, iterations=3, seed=39, ensemble_size=2)
    events_path = tmp_path / "verification" / "data" / "pregeometry" / "runs" / "dash_pr1" / "events.jsonl"
    summary_path = tmp_path / "verification" / "data" / "pregeometry" / "runs" / "dash_pr1" / "summary.json"
    before_events = events_path.read_bytes()
    before_summary = summary_path.read_bytes()
    panel = render_dashboard_snapshot(read_summary(tmp_path, "dash_pr1"), read_events(tmp_path, "dash_pr1"), project_root=tmp_path)
    assert panel is not None
    assert events_path.read_bytes() == before_events
    assert summary_path.read_bytes() == before_summary


def test_pr1_summary_json_contains_only_registered_metric_claim_boundary(tmp_path: Path) -> None:
    result = run_pr1_null_ensembles(project_root=tmp_path, iterations=4, seed=39, ensemble_size=3)
    summary = json.loads((tmp_path / Path(str(result["summary_json"]))).read_text(encoding="utf-8"))
    assert summary["scientific_status"]["null_model_separation_metrics"] == "[D]"
    assert summary["scientific_status"]["physical_interpretation"] == "[D/E]"
    assert len(summary["metrics"]) == 4
    assert all(row["interpretation_boundary"] == "distinguishability from selected nulls only" for row in summary["metrics"])

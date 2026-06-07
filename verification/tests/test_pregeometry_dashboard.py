from __future__ import annotations

import importlib.util
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError
from rich.console import Console

from verification.pregeometry.dashboard.renderers import render_dashboard_snapshot
from verification.pregeometry.dashboard.renderers import (
    render_null_model_panel,
    sparkline,
)
from verification.pregeometry.dashboard.rich_snapshot import TEXTUAL_MISSING_WARNING, render_snapshot
from verification.pregeometry.dashboard.runtime import has_textual
from verification.pregeometry.dashboard.schemas import (
    FORBIDDEN_VISUALIZATION_LABELS,
    InvariantBlock,
    TelemetryEvent,
    assert_no_forbidden_visualization_text,
)
from verification.pregeometry.dashboard.telemetry import (
    append_event,
    build_diagnostics,
    compute_event_file_hash,
    ensure_allowed_telemetry_path,
    list_runs,
    read_events,
    read_events_validated,
    read_summary,
    resolve_latest_run,
    validate_event_count_against_summary,
    validate_monotonic_ticks,
)
from verification.pregeometry.experiments.run_pregeometry_toy import run_pr0


def _valid_event(**overrides: object) -> TelemetryEvent:
    payload = {
        "run_id": "test_run_001",
        "tick": 1,
        "seed": 39,
        "model": "uidt_toy_pr0",
        "rule": "rule_empty_to_first_distinction",
        "N": 1,
        "E": 0,
        "C": 1,
        "beta_1": 0,
        "acyclic": True,
        "leakage_passed": True,
        "invariant_passed": True,
        "claim_status": "[D/E]",
        "timestamp_utc": datetime.now(timezone.utc),
    }
    payload.update(overrides)
    return TelemetryEvent.model_validate(payload)


def test_telemetry_schema_accepts_valid_event() -> None:
    event = _valid_event()
    assert event.schema_version == "pr0.telemetry.v1"
    assert event.claim_status == "[D/E]"
    assert event.invariants() == InvariantBlock(N=1, E=0, C=1, beta_1=0)


def test_telemetry_schema_rejects_malformed_boolean_and_negative_invariant() -> None:
    with pytest.raises(ValidationError):
        _valid_event(acyclic="true")
    with pytest.raises(ValidationError):
        _valid_event(N=-1)
    with pytest.raises(ValidationError):
        _valid_event(N=2, E=0, C=0, beta_1=0)


def test_forbidden_visualization_labels_are_rejected() -> None:
    for label in FORBIDDEN_VISUALIZATION_LABELS:
        with pytest.raises(ValueError):
            assert_no_forbidden_visualization_text(f"debug label: {label}")


def test_dashboard_readers_do_not_mutate_events_jsonl(tmp_path: Path) -> None:
    project_root = tmp_path
    event = _valid_event()
    path = append_event(project_root, event)
    before = path.read_bytes()
    events = read_events(project_root, event.run_id)
    after = path.read_bytes()
    assert events == (event,)
    assert after == before


def test_root_export_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(AssertionError):
        ensure_allowed_telemetry_path(tmp_path / "events.jsonl", project_root=tmp_path)


def test_run_pr0_telemetry_creates_events_and_summary_under_allowed_tree(tmp_path: Path) -> None:
    result = run_pr0(
        project_root=tmp_path,
        iterations=4,
        seed=39,
        telemetry=True,
        run_id="test_run_telemetry",
    )
    events_rel = Path(str(result["telemetry_events"]))
    summary_rel = Path(str(result["telemetry_summary"]))

    assert events_rel.parts[:4] == ("verification", "data", "pregeometry", "runs")
    assert summary_rel.parts[:4] == ("verification", "data", "pregeometry", "runs")

    events = read_events(tmp_path, "test_run_telemetry")
    summary = read_summary(tmp_path, "test_run_telemetry")
    assert len(events) == 4
    assert summary.event_count == 4
    assert summary.claim_status == "[D/E]"
    assert summary.latest_event == events[-1]


def test_run_browser_resolves_latest_and_lists_runs(tmp_path: Path) -> None:
    run_pr0(project_root=tmp_path, iterations=2, seed=39, telemetry=True, run_id="run_a")
    run_pr0(project_root=tmp_path, iterations=3, seed=39, telemetry=True, run_id="run_b")
    entries = list_runs(tmp_path)
    assert {entry.run_id for entry in entries} == {"run_a", "run_b"}
    assert resolve_latest_run(tmp_path) in {"run_a", "run_b"}
    assert all(entry.events_sha256 for entry in entries)


def test_event_reader_validates_every_event_and_hashes_read_only(tmp_path: Path) -> None:
    run_pr0(project_root=tmp_path, iterations=3, seed=39, telemetry=True, run_id="hash_run")
    event_path = tmp_path / "verification" / "data" / "pregeometry" / "runs" / "hash_run" / "events.jsonl"
    before = event_path.read_bytes()
    digest = compute_event_file_hash(event_path)
    events = read_events_validated(event_path)
    after = event_path.read_bytes()
    assert len(events) == 3
    assert len(digest) == 64
    assert before == after


def test_summary_reader_does_not_mutate_summary_json(tmp_path: Path) -> None:
    run_pr0(project_root=tmp_path, iterations=3, seed=39, telemetry=True, run_id="summary_read")
    summary_file = tmp_path / "verification" / "data" / "pregeometry" / "runs" / "summary_read" / "summary.json"
    before = summary_file.read_bytes()
    summary = read_summary(tmp_path, "summary_read")
    after = summary_file.read_bytes()
    assert summary.run_id == "summary_read"
    assert before == after


def test_monotonic_ticks_pass_and_fail() -> None:
    events = (
        _valid_event(tick=1),
        _valid_event(tick=2, N=2, E=1, C=1, beta_1=0),
    )
    bad = (events[1], events[0])
    assert validate_monotonic_ticks(events)
    assert not validate_monotonic_ticks(bad)


def test_diagnostics_detect_event_count_mismatch(tmp_path: Path) -> None:
    run_pr0(project_root=tmp_path, iterations=3, seed=39, telemetry=True, run_id="diag_run")
    events = read_events(tmp_path, "diag_run")
    summary = read_summary(tmp_path, "diag_run")
    shorter = events[:-1]
    diagnostics = build_diagnostics(project_root=tmp_path, events=shorter, summary=summary)
    assert not validate_event_count_against_summary(shorter, summary)
    assert diagnostics.event_count_consistency is False


def test_null_model_comparison_tolerates_missing_data() -> None:
    panel = render_null_model_panel(None, None)
    assert "unavailable" in str(panel.renderable)


def test_sparkline_is_telemetry_only_compact_series() -> None:
    assert sparkline([1, 2, 3, 4])
    assert sparkline([5, 5, 5]) == "▁▁▁"


def test_rich_renderers_produce_non_physical_dashboard_text(tmp_path: Path) -> None:
    run_pr0(
        project_root=tmp_path,
        iterations=3,
        seed=39,
        telemetry=True,
        run_id="test_run_render",
    )
    events = read_events(tmp_path, "test_run_render")
    summary = read_summary(tmp_path, "test_run_render")

    console = Console(record=True, width=120)
    console.print(render_dashboard_snapshot(summary, events, project_root=tmp_path, run_entries=list_runs(tmp_path)))
    rendered = console.export_text()

    assert "graph invariant telemetry" in rendered
    assert "Run Browser" in rendered
    assert "Time-Series" in rendered
    assert "Diagnostics" in rendered
    assert "[D/E]" in rendered
    for label in FORBIDDEN_VISUALIZATION_LABELS:
        assert label not in rendered


def test_runtime_detects_textual_when_installed() -> None:
    assert has_textual() is True


def test_runtime_reports_textual_missing_when_find_spec_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import verification.pregeometry.dashboard.runtime as runtime

    original_find_spec = importlib.util.find_spec

    def fake_find_spec(name: str, package: str | None = None):
        if name == "textual":
            return None
        return original_find_spec(name, package)

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)
    assert runtime.has_textual() is False


def test_rich_fallback_prints_explicit_warning(tmp_path: Path) -> None:
    run_pr0(
        project_root=tmp_path,
        iterations=2,
        seed=39,
        telemetry=True,
        run_id="test_run_fallback",
    )
    console = Console(record=True, width=120)
    render_snapshot(
        project_root=tmp_path,
        run="test_run_fallback",
        warning=TEXTUAL_MISSING_WARNING,
        console=console,
    )
    rendered = console.export_text()
    assert TEXTUAL_MISSING_WARNING in rendered
    assert "[D/E]" in rendered


def test_dashboard_dispatches_to_textual_path_when_available(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from verification.pregeometry.dashboard import tui_app

    calls = []

    def fake_has_textual() -> bool:
        return True

    def fake_run_textual_app(*, project_root: Path, run: str) -> None:
        calls.append((project_root, run))

    monkeypatch.setattr(tui_app, "has_textual", fake_has_textual)
    import verification.pregeometry.dashboard.textual_app as textual_app

    monkeypatch.setattr(textual_app, "run_textual_app", fake_run_textual_app)
    result = tui_app.dispatch_dashboard(project_root=tmp_path, run="latest")
    assert result == "textual"
    assert calls == [(tmp_path, "latest")]


def test_textual_app_can_be_instantiated_without_network_access(tmp_path: Path) -> None:
    from verification.pregeometry.dashboard.textual_app import build_textual_app

    run_pr0(project_root=tmp_path, iterations=2, seed=39, telemetry=True, run_id="textual_inst")
    app_cls = build_textual_app(project_root=tmp_path, run="textual_inst")
    app = app_cls()
    assert app.TITLE == "UIDT PR-0.6 Pregeometry Telemetry Cockpit"


def test_dashboard_dispatches_to_rich_fallback_when_textual_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from verification.pregeometry.dashboard import tui_app

    calls = []

    def fake_has_textual() -> bool:
        return False

    def fake_render_snapshot(*, project_root: Path, run: str, warning: str | None = None) -> None:
        calls.append((project_root, run, warning))

    monkeypatch.setattr(tui_app, "has_textual", fake_has_textual)
    monkeypatch.setattr(tui_app, "render_snapshot", fake_render_snapshot)
    result = tui_app.dispatch_dashboard(project_root=tmp_path, run="latest")
    assert result == "rich"
    assert calls == [(tmp_path, "latest", TEXTUAL_MISSING_WARNING)]

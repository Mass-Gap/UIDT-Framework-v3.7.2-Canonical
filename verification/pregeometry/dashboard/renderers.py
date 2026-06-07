"""Rich renderers for PR-0.6 telemetry cockpit panels."""

from __future__ import annotations

import json
from pathlib import Path

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from verification.pregeometry.dashboard.schemas import RunSummary, TelemetryEvent, assert_no_forbidden_visualization_text
from verification.pregeometry.dashboard.telemetry import (
    DashboardDiagnostics,
    RunBrowserEntry,
    build_diagnostics,
    compute_event_file_hash,
    events_path,
    list_runs,
    summarize_event_series,
    summary_path,
)


SAFE_LIMITATIONS = (
    "This dashboard is a passive telemetry viewer for a restricted PR-0 toy sector.",
    "It does not establish metric emergence, cosmology validity, gauge-sector emergence, or physical correctness.",
    "Physical interpretation remains [D/E].",
)


def sparkline(values: list[int] | tuple[int, ...]) -> str:
    """Return a compact sparkline for integer telemetry values."""
    if not values:
        return ""
    marks = "▁▂▃▄▅▆▇█"
    lo = min(values)
    hi = max(values)
    if lo == hi:
        return marks[0] * len(values)
    scale = len(marks) - 1
    return "".join(marks[(value - lo) * scale // (hi - lo)] for value in values)


def render_dashboard_snapshot(
    summary: RunSummary,
    events: tuple[TelemetryEvent, ...],
    *,
    project_root: Path | None = None,
    run_entries: tuple[RunBrowserEntry, ...] = (),
) -> Group:
    """Return a static Rich cockpit snapshot with conservative labels."""
    diagnostics = build_diagnostics(
        project_root=project_root or Path("."),
        events=events,
        summary=summary,
        rendered_text=" ".join(SAFE_LIMITATIONS),
    )
    assert_no_forbidden_visualization_text(
        [
            "UIDT PR-0.6 Pregeometry Telemetry Cockpit",
            "coordinate-free relational carrier",
            "graph invariant telemetry",
            *SAFE_LIMITATIONS,
        ]
    )
    return Group(
        render_run_browser(run_entries),
        render_header(summary, events, project_root=project_root),
        render_invariant_panel(events, summary),
        render_time_series_panel(events),
        render_event_log(events),
        render_event_inspector(events[-1] if events else None),
        render_null_model_panel(summary, events[-1] if events else None),
        render_diagnostics_panel(diagnostics),
        render_limitations_panel(),
    )


def render_run_browser(entries: tuple[RunBrowserEntry, ...]) -> Table:
    table = Table(title="Run Browser")
    table.add_column("run_id")
    table.add_column("events", justify="right")
    table.add_column("summary")
    table.add_column("last_modified")
    table.add_column("events_sha256")
    for entry in entries[:8]:
        table.add_row(
            entry.run_id,
            str(entry.event_count),
            entry.summary_status,
            entry.last_modified.isoformat() if entry.last_modified else "-",
            (entry.events_sha256 or "-")[:12],
        )
    if not entries:
        table.add_row("No runs found", "0", "-", "-", "-")
    return table


def render_header(summary: RunSummary, events: tuple[TelemetryEvent, ...], *, project_root: Path | None = None) -> Panel:
    latest = events[-1] if events else summary.latest_event
    event_hash = "-"
    summary_hash = "-"
    if project_root is not None:
        event_file = events_path(project_root, summary.run_id)
        summary_file = summary_path(project_root, summary.run_id)
        if event_file.exists():
            event_hash = compute_event_file_hash(event_file)[:16]
        if summary_file.exists():
            summary_hash = compute_event_file_hash(summary_file)[:16]

    text = Text()
    text.append("UIDT PR-0.6 Pregeometry Telemetry Cockpit\n", style="bold")
    text.append("graph invariant telemetry | coordinate-free relational carrier\n")
    text.append(f"run_id: {summary.run_id} | seed: {summary.seed} | ticks: {len(events)} | status: OK\n")
    text.append(
        f"schema: {summary.schema_version} | model: {(latest.model if latest else 'unknown')} | "
        f"claim: {summary.claim_status} | read_only: true\n"
    )
    text.append(
        f"leakage: {_pass(summary.leakage_passed)} | invariant health: {_pass(summary.invariant_passed)} | "
        f"events_sha256: {event_hash} | summary_sha256: {summary_hash}"
    )
    return Panel(text, title="Header Metadata")


def render_invariant_panel(events: tuple[TelemetryEvent, ...], summary: RunSummary) -> Table:
    series = summarize_event_series(events)
    latest = series.latest or summary.latest_event
    delta = series.latest_delta
    table = Table(title="Exact Invariants")
    table.add_column("field")
    table.add_column("latest", justify="right")
    table.add_column("delta", justify="right")
    if latest is None:
        table.add_row("N", "-", "-")
        table.add_row("E", "-", "-")
        table.add_row("C", "-", "-")
        table.add_row("beta_1", "-", "-")
    else:
        table.add_row("N", str(latest.N), f"+{delta.N}")
        table.add_row("E", str(latest.E), f"+{delta.E}")
        table.add_row("C", str(latest.C), f"+{delta.C}")
        table.add_row("beta_1", str(latest.beta_1), f"+{delta.beta_1}")
        table.add_row("acyclic", str(latest.acyclic).lower(), "")
        table.add_row("leakage_passed", str(latest.leakage_passed).lower(), "")
        table.add_row("invariant_passed", str(latest.invariant_passed).lower(), "")
    return table


def render_time_series_panel(events: tuple[TelemetryEvent, ...]) -> Panel:
    series = summarize_event_series(events)
    body = "\n".join(
        [
            f"N(t)      {sparkline(series.N_values)}",
            f"E(t)      {sparkline(series.E_values)}",
            f"beta_1(t) {sparkline(series.beta_1_values)}",
        ]
    )
    return Panel(body, title="Time-Series")


def render_event_log(events: tuple[TelemetryEvent, ...], *, limit: int = 16) -> Table:
    table = Table(title="Rule Event Log")
    for column in ("tick", "timestamp_utc", "rule", "N", "E", "C", "beta_1", "acyclic", "leakage", "invariant"):
        table.add_column(column, justify="right" if column in {"tick", "N", "E", "C", "beta_1"} else "left")
    for event in events[-limit:]:
        table.add_row(
            f"{event.tick:04d}",
            event.timestamp_utc.isoformat(),
            event.rule,
            str(event.N),
            str(event.E),
            str(event.C),
            str(event.beta_1),
            str(event.acyclic).lower(),
            _pass(event.leakage_passed),
            _pass(event.invariant_passed),
        )
    return table


def render_event_inspector(event: TelemetryEvent | None) -> Panel:
    if event is None:
        return Panel("No selected event.", title="Event Inspector")
    validated = TelemetryEvent.model_validate(event.model_dump())
    payload = json.dumps(validated.model_dump(mode="json"), indent=2, sort_keys=True)
    return Panel(payload, title="Event Inspector")


def render_null_model_panel(summary: RunSummary | None, latest: TelemetryEvent | None) -> Table | Panel:
    if summary is None or latest is None:
        return Panel("Null-model comparison unavailable for this run", title="Null Model Comparison")
    row = summary.null_model_row
    inv = row.invariants
    table = Table(title="Null Model Comparison")
    for column in ("model", "N", "E", "C", "beta_1", "delta_N", "delta_E", "delta_beta_1", "status"):
        table.add_column(column, justify="right" if column != "model" and column != "status" else "left")
    table.add_row(
        row.name,
        str(inv.N),
        str(inv.E),
        str(inv.C),
        str(inv.beta_1),
        str(inv.N - latest.N),
        str(inv.E - latest.E),
        str(inv.beta_1 - latest.beta_1),
        row.claim_status,
    )
    return table


def render_diagnostics_panel(diagnostics: DashboardDiagnostics) -> Table:
    table = Table(title="Diagnostics")
    table.add_column("check")
    table.add_column("status")
    table.add_row("forbidden label scan", _pass(diagnostics.forbidden_label_scan))
    table.add_row("root export rejected", _pass(diagnostics.root_export_rejected))
    table.add_row("append-only telemetry", diagnostics.append_only_telemetry)
    table.add_row("schema validity", _pass(diagnostics.schema_validity))
    table.add_row("event count consistency", _pass(diagnostics.event_count_consistency))
    table.add_row("monotonic tick order", _pass(diagnostics.monotonic_tick_order))
    table.add_row("timestamp UTC validity", _pass(diagnostics.timestamp_utc_validity))
    table.add_row("primitive coordinate input", "ABSENT")
    table.add_row("target metric input", "ABSENT")
    return table


def render_limitations_panel() -> Panel:
    return Panel("\n".join(f"- {item}" for item in SAFE_LIMITATIONS), title="Limitations")


def _pass(value: bool) -> str:
    return "PASS" if value else "FAIL"

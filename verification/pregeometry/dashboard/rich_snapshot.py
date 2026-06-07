"""Explicit Rich read-only fallback for PR-0.5 telemetry."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

from verification.pregeometry.dashboard.renderers import render_dashboard_snapshot
from verification.pregeometry.dashboard.telemetry import list_runs, read_events, read_summary, resolve_latest_run


TEXTUAL_MISSING_WARNING = "[WARN] Textual not installed; rendering Rich read-only snapshot."


def load_dashboard_data(*, project_root: Path, run: str):
    """Load read-only telemetry data for a dashboard run."""
    run_id = resolve_latest_run(project_root) if run == "latest" else run
    summary = read_summary(project_root, run_id)
    events = read_events(project_root, run_id)
    return summary, events


def render_snapshot(
    *,
    project_root: Path,
    run: str,
    warning: str | None = None,
    console: Console | None = None,
) -> None:
    """Render a read-only Rich snapshot of existing telemetry."""
    target_console = console or Console()
    summary, events = load_dashboard_data(project_root=project_root, run=run)
    if warning:
        target_console.print(warning)
    target_console.print(
        render_dashboard_snapshot(
            summary,
            events,
            project_root=project_root,
            run_entries=list_runs(project_root),
        )
    )

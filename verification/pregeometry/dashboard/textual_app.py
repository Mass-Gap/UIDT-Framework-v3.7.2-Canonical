"""Primary Textual TUI for the PR-0.6 telemetry cockpit."""

from __future__ import annotations

from pathlib import Path

from verification.pregeometry.dashboard.rich_snapshot import load_dashboard_data
from verification.pregeometry.dashboard.renderers import (
    render_diagnostics_panel,
    render_event_inspector,
    render_event_log,
    render_header,
    render_invariant_panel,
    render_limitations_panel,
    render_null_model_panel,
    render_run_browser,
    render_time_series_panel,
)
from verification.pregeometry.dashboard.telemetry import build_diagnostics, list_runs


def build_textual_app(*, project_root: Path, run: str):
    """Build the Textual app class without launching it."""
    from textual.app import App, ComposeResult
    from textual.containers import Grid, VerticalScroll
    from textual.widgets import DataTable, Footer, Header, Static

    class TelemetryCockpitApp(App[None]):
        TITLE = "UIDT PR-0.6 Pregeometry Telemetry Cockpit"
        BINDINGS = [
            ("r", "reload", "Reload"),
            ("q", "quit", "Quit"),
            ("enter", "inspect", "Inspect"),
            ("up", "cursor_up", "Up"),
            ("down", "cursor_down", "Down"),
        ]

        def __init__(self) -> None:
            super().__init__()
            self.project_root = Path(project_root)
            self.selected_run_id = run
            self.summary, self.events = load_dashboard_data(project_root=self.project_root, run=self.selected_run_id)
            self.selected_index = max(len(self.events) - 1, 0)

        def compose(self) -> ComposeResult:
            yield Header()
            with Grid(id="cockpit"):
                yield Static(id="run_browser")
                yield Static(id="header_meta")
                yield Static(id="invariants")
                yield Static(id="series")
                yield DataTable(id="event_table")
                yield Static(id="inspector")
                yield Static(id="null_model")
                yield Static(id="diagnostics")
                yield Static(id="limitations")
            yield Footer()

        def on_mount(self) -> None:
            self._refresh_widgets()

        def action_reload(self) -> None:
            self.summary, self.events = load_dashboard_data(project_root=self.project_root, run=self.selected_run_id)
            self.selected_index = min(self.selected_index, max(len(self.events) - 1, 0))
            self._refresh_widgets()

        def action_inspect(self) -> None:
            self._refresh_inspector()

        def action_cursor_up(self) -> None:
            if self.events:
                self.selected_index = max(self.selected_index - 1, 0)
                self._refresh_inspector()

        def action_cursor_down(self) -> None:
            if self.events:
                self.selected_index = min(self.selected_index + 1, len(self.events) - 1)
                self._refresh_inspector()

        def _refresh_widgets(self) -> None:
            latest = self.events[-1] if self.events else None
            diagnostics = build_diagnostics(
                project_root=self.project_root,
                events=self.events,
                summary=self.summary,
                rendered_text="",
            )
            self.query_one("#run_browser", Static).update(render_run_browser(list_runs(self.project_root)))
            self.query_one("#header_meta", Static).update(render_header(self.summary, self.events, project_root=self.project_root))
            self.query_one("#invariants", Static).update(render_invariant_panel(self.events, self.summary))
            self.query_one("#series", Static).update(render_time_series_panel(self.events))
            self.query_one("#null_model", Static).update(render_null_model_panel(self.summary, latest))
            self.query_one("#diagnostics", Static).update(render_diagnostics_panel(diagnostics))
            self.query_one("#limitations", Static).update(render_limitations_panel())
            self._refresh_event_table()
            self._refresh_inspector()

        def _refresh_event_table(self) -> None:
            table = self.query_one("#event_table", DataTable)
            table.clear(columns=True)
            for column in ("tick", "timestamp_utc", "rule", "N", "E", "C", "beta_1", "acyclic", "leakage", "invariant"):
                table.add_column(column)
            for event in self.events:
                table.add_row(
                    f"{event.tick:04d}",
                    event.timestamp_utc.isoformat(),
                    event.rule,
                    str(event.N),
                    str(event.E),
                    str(event.C),
                    str(event.beta_1),
                    str(event.acyclic).lower(),
                    str(event.leakage_passed).lower(),
                    str(event.invariant_passed).lower(),
                )

        def _refresh_inspector(self) -> None:
            selected = self.events[self.selected_index] if self.events else None
            self.query_one("#inspector", Static).update(render_event_inspector(selected))

    return TelemetryCockpitApp


def run_textual_app(*, project_root: Path, run: str) -> None:
    """Launch the primary Textual dashboard path."""
    app_or_factory = build_textual_app(project_root=project_root, run=run)
    app = app_or_factory() if isinstance(app_or_factory, type) else app_or_factory
    assert callable(app.run), "Textual App.run() was shadowed or is not callable"
    app.run()

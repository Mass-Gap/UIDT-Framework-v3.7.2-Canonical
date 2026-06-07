"""Append-only telemetry I/O for the UIDT PR-0.5 dashboard."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from verification.pregeometry.dashboard.schemas import (
    InvariantBlock,
    NullModelRow,
    RunSummary,
    TelemetryEvent,
    assert_no_forbidden_visualization_text,
)


def make_run_id(*, seed: int, iterations: int, timestamp: datetime | None = None) -> str:
    """Return a filename-safe run id."""
    stamp = (timestamp or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return f"{stamp:%Y%m%dT%H%M%SZ}_seed{seed}_iter{iterations}"


def runs_root(project_root: Path) -> Path:
    return Path(project_root).resolve() / "verification" / "data" / "pregeometry" / "runs"


def run_directory(project_root: Path, run_id: str) -> Path:
    # Validation is delegated to TelemetryEvent/RunSummary patterns at write time.
    return runs_root(project_root) / run_id


def events_path(project_root: Path, run_id: str) -> Path:
    return run_directory(project_root, run_id) / "events.jsonl"


def summary_path(project_root: Path, run_id: str) -> Path:
    return run_directory(project_root, run_id) / "summary.json"


def ensure_allowed_telemetry_path(path: Path, *, project_root: Path) -> None:
    """Reject root and out-of-tree telemetry paths."""
    resolved = Path(path).resolve()
    root = Path(project_root).resolve()
    allowed_root = runs_root(root).resolve()
    if resolved.parent == root:
        raise AssertionError(f"Refusing telemetry output at repository root: {resolved}")
    try:
        resolved.relative_to(allowed_root)
    except ValueError as exc:
        raise AssertionError(f"Telemetry path is outside allowed run directory: {resolved}") from exc


def append_event(project_root: Path, event: TelemetryEvent) -> Path:
    path = events_path(project_root, event.run_id)
    ensure_allowed_telemetry_path(path, project_root=project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(event.model_dump_json() + "\n")
    return path


def read_events(project_root: Path, run_id: str) -> tuple[TelemetryEvent, ...]:
    path = events_path(project_root, run_id)
    ensure_allowed_telemetry_path(path, project_root=project_root)
    return read_events_validated(path)


def read_events_validated(path: Path) -> tuple[TelemetryEvent, ...]:
    """Read and validate every event in an events JSONL file."""
    if not path.exists():
        return ()
    return tuple(
        TelemetryEvent.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def write_summary(project_root: Path, summary: RunSummary) -> Path:
    path = summary_path(project_root, summary.run_id)
    ensure_allowed_telemetry_path(path, project_root=project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(summary.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return path


def read_summary(project_root: Path, run_id: str) -> RunSummary:
    path = summary_path(project_root, run_id)
    ensure_allowed_telemetry_path(path, project_root=project_root)
    return RunSummary.model_validate_json(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class RunBrowserEntry:
    run_id: str
    event_count: int
    summary_status: str
    last_modified: datetime | None
    events_sha256: str | None
    summary_sha256: str | None


@dataclass(frozen=True)
class EventSeriesSummary:
    event_count: int
    latest: TelemetryEvent | None
    previous: TelemetryEvent | None
    N_values: tuple[int, ...]
    E_values: tuple[int, ...]
    C_values: tuple[int, ...]
    beta_1_values: tuple[int, ...]

    @property
    def latest_delta(self) -> InvariantBlock:
        if self.latest is None:
            return InvariantBlock(N=0, E=0, C=0, beta_1=0)
        if self.previous is None:
            return InvariantBlock(N=0, E=0, C=0, beta_1=0)
        return InvariantBlock(
            N=max(self.latest.N - self.previous.N, 0),
            E=max(self.latest.E - self.previous.E, 0),
            C=max(self.latest.C - self.previous.C, 0),
            beta_1=max(self.latest.beta_1 - self.previous.beta_1, 0),
        )


@dataclass(frozen=True)
class DashboardDiagnostics:
    forbidden_label_scan: bool
    root_export_rejected: bool
    append_only_telemetry: str
    schema_validity: bool
    event_count_consistency: bool
    monotonic_tick_order: bool
    timestamp_utc_validity: bool



def resolve_latest_run(project_root: Path) -> str:
    root = runs_root(project_root)
    if not root.exists():
        raise FileNotFoundError("No PR-0.5 telemetry runs found.")
    candidates = [path for path in root.iterdir() if path.is_dir()]
    if not candidates:
        raise FileNotFoundError("No PR-0.5 telemetry runs found.")
    newest = max(candidates, key=lambda path: _run_mtime(path))
    return newest.name


def list_runs(project_root: Path) -> tuple[RunBrowserEntry, ...]:
    """Return read-only metadata for available telemetry runs."""
    root = runs_root(project_root)
    if not root.exists():
        return ()
    entries = []
    for path in sorted((item for item in root.iterdir() if item.is_dir()), key=_run_mtime, reverse=True):
        event_path = path / "events.jsonl"
        summary_file = path / "summary.json"
        try:
            events = read_events_validated(event_path) if event_path.exists() else ()
            summary_status = "PASS" if summary_file.exists() else "MISSING"
        except Exception:
            events = ()
            summary_status = "INVALID"
        latest_mtime = _run_mtime(path)
        entries.append(
            RunBrowserEntry(
                run_id=path.name,
                event_count=len(events),
                summary_status=summary_status,
                last_modified=datetime.fromtimestamp(latest_mtime, tz=timezone.utc) if latest_mtime else None,
                events_sha256=compute_event_file_hash(event_path) if event_path.exists() else None,
                summary_sha256=compute_event_file_hash(summary_file) if summary_file.exists() else None,
            )
        )
    return tuple(entries)


def compute_event_file_hash(path: Path) -> str:
    """Return a read-only SHA256 hash for an event or summary file."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarize_event_series(events: Sequence[TelemetryEvent]) -> EventSeriesSummary:
    ordered = tuple(events)
    return EventSeriesSummary(
        event_count=len(ordered),
        latest=ordered[-1] if ordered else None,
        previous=ordered[-2] if len(ordered) > 1 else None,
        N_values=tuple(event.N for event in ordered),
        E_values=tuple(event.E for event in ordered),
        C_values=tuple(event.C for event in ordered),
        beta_1_values=tuple(event.beta_1 for event in ordered),
    )


def validate_monotonic_ticks(events: Sequence[TelemetryEvent]) -> bool:
    ticks = [event.tick for event in events]
    return ticks == sorted(ticks) and len(ticks) == len(set(ticks))


def validate_event_count_against_summary(events: Sequence[TelemetryEvent], summary: RunSummary) -> bool:
    return len(events) == summary.event_count


def validate_timestamp_utc(events: Sequence[TelemetryEvent]) -> bool:
    return all(event.timestamp_utc.tzinfo is not None and event.timestamp_utc.utcoffset() is not None for event in events)


def validate_forbidden_labels_in_rendered_text(text: str) -> bool:
    try:
        assert_no_forbidden_visualization_text(text)
    except ValueError:
        return False
    return True


def build_diagnostics(
    *,
    project_root: Path,
    events: Sequence[TelemetryEvent],
    summary: RunSummary,
    rendered_text: str = "",
) -> DashboardDiagnostics:
    root_rejected = False
    try:
        ensure_allowed_telemetry_path(Path(project_root) / "events.jsonl", project_root=project_root)
    except AssertionError:
        root_rejected = True
    return DashboardDiagnostics(
        forbidden_label_scan=validate_forbidden_labels_in_rendered_text(rendered_text),
        root_export_rejected=root_rejected,
        append_only_telemetry="UNKNOWN",
        schema_validity=True,
        event_count_consistency=validate_event_count_against_summary(events, summary),
        monotonic_tick_order=validate_monotonic_ticks(events),
        timestamp_utc_validity=validate_timestamp_utc(events),
    )


def make_event(
    *,
    run_id: str,
    tick: int,
    seed: int,
    rule: str,
    invariants: InvariantBlock,
    acyclic: bool,
    leakage_passed: bool,
    invariant_passed: bool,
    timestamp_utc: datetime | None = None,
) -> TelemetryEvent:
    return TelemetryEvent(
        run_id=run_id,
        tick=tick,
        seed=seed,
        model="uidt_toy_pr0",
        rule=rule,
        N=invariants.N,
        E=invariants.E,
        C=invariants.C,
        beta_1=invariants.beta_1,
        acyclic=acyclic,
        leakage_passed=leakage_passed,
        invariant_passed=invariant_passed,
        claim_status="[D/E]",
        timestamp_utc=timestamp_utc or datetime.now(timezone.utc),
    )


def make_summary(
    *,
    run_id: str,
    seed: int,
    iterations: int,
    null_model: str,
    events: Sequence[TelemetryEvent],
    uidt_invariants: InvariantBlock,
    null_invariants: InvariantBlock,
    leakage_passed: bool,
    invariant_passed: bool,
    run_json: str,
    report: str,
) -> RunSummary:
    return RunSummary(
        run_id=run_id,
        seed=seed,
        iterations=iterations,
        null_model=null_model,
        event_count=len(events),
        latest_event=events[-1] if events else None,
        uidt_invariants=uidt_invariants,
        null_model_row=NullModelRow(name=null_model, invariants=null_invariants),
        leakage_passed=leakage_passed,
        invariant_passed=invariant_passed,
        claim_status="[D/E]",
        run_json=run_json,
        report=report,
    )


def _run_mtime(path: Path) -> float:
    files = [path / "summary.json", path / "events.jsonl"]
    existing = [item.stat().st_mtime for item in files if item.exists()]
    return max(existing) if existing else path.stat().st_mtime

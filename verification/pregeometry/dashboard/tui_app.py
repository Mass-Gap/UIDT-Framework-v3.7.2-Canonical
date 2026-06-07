"""Entrypoint for the passive PR-0.5 dashboard."""

from __future__ import annotations

import argparse
from pathlib import Path

from verification.pregeometry.dashboard.rich_snapshot import TEXTUAL_MISSING_WARNING, render_snapshot
from verification.pregeometry.dashboard.runtime import has_textual


def main() -> None:
    args = _parse_args()
    dispatch_dashboard(project_root=Path(args.project_root).resolve(), run=args.run)


def dispatch_dashboard(*, project_root: Path, run: str) -> str:
    """Dispatch to Textual when available, otherwise to explicit Rich fallback."""
    if has_textual():
        from verification.pregeometry.dashboard.textual_app import run_textual_app

        run_textual_app(project_root=project_root, run=run)
        return "textual"

    render_snapshot(
        project_root=project_root,
        run=run,
        warning=TEXTUAL_MISSING_WARNING,
    )
    return "rich"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only UIDT PR-0.5 telemetry dashboard.")
    parser.add_argument("--run", default="latest", help="Run id to open, or 'latest'.")
    parser.add_argument("--project-root", default=".")
    return parser.parse_args()


if __name__ == "__main__":
    main()

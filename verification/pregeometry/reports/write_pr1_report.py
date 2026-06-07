"""Write the PR-1 null-ensemble report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from verification.pregeometry.dashboard.schemas import assert_no_forbidden_visualization_text


REPORT_RELATIVE_PATH = Path("verification") / "pregeometry" / "reports" / "pr1_null_ensemble_report.md"


def write_pr1_report(*, project_root: Path, summary: Mapping[str, object]) -> Path:
    path = Path(project_root).resolve() / REPORT_RELATIVE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    text = build_pr1_report_text(summary)
    assert_no_forbidden_visualization_text(text)
    path.write_text(text, encoding="utf-8")
    return path


def build_pr1_report_text(summary: Mapping[str, object]) -> str:
    parameters = summary["parameters"]
    toy = summary["pr0_toy"]
    metrics = summary["metrics"]
    lines = [
        "# PR-1 Null-Ensemble Separation Report",
        "",
        "Status: advisory software benchmark report for a separate experimental pregeometry workspace.",
        "",
        "## Claims Table",
        "",
        "| Claim | Status | Boundary |",
        "|---|---:|---|",
        "| Exact PR-0 integer invariants were reproduced for this executed software path. | [A] | Software path only. |",
        "| Null-ensemble separation metrics were computed. | [D] | Distinguishability from selected nulls only. |",
        "| Physical interpretation of the benchmark remains limited. | [D/E] | Outside PR-1 scope. |",
        "",
        "## Reproduction Note",
        "",
        "```powershell",
        (
            "py -m verification.pregeometry.experiments.run_pr1_null_ensembles "
            f"--iterations {parameters['iterations']} --seed {parameters['seed']} "
            f"--ensemble-size {parameters['ensemble_size']}"
        ),
        "```",
        "",
        "## PR-0 Toy Final Invariants",
        "",
        "| N | E | C | beta_1 |",
        "|---:|---:|---:|---:|",
        (
            f"| {toy['final_invariants']['N']} | {toy['final_invariants']['E']} | "
            f"{toy['final_invariants']['C']} | {toy['final_invariants']['beta_1']} |"
        ),
        "",
        "## Registered Metric Results",
        "",
        "| Ensemble | Members | Final L1 mean | Trajectory L1 mean | Wasserstein mean | Permutation p |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in metrics:
        lines.append(
            "| {ensemble} | {members} | {final_l1} | {trajectory_l1} | {wasserstein} | {p_value} |".format(
                ensemble=row["ensemble"],
                members=row["member_count"],
                final_l1=row["final_state_l1_mean"]["decimal"],
                trajectory_l1=row["trajectory_l1_mean"]["decimal"],
                wasserstein=row["wasserstein_mean"]["decimal"],
                p_value=row["permutation_p_value"]["decimal"],
            )
        )
    lines.extend(
        [
            "",
            "## Negative Results And Limitations",
            "",
            "A nonzero distance is only a software distinguishability statement against the selected null ensembles.",
            "Physical interpretation remains outside the scope of this benchmark.",
            "Post-hoc metric selection is not used; the registered metric list is fixed in `PRE_REGISTERED_PR1_METRICS.md`.",
            "",
            "## Machine Summary",
            "",
            "```json",
            json.dumps(summary, indent=2, sort_keys=True),
            "```",
            "",
        ]
    )
    return "\n".join(lines)

"""Report generator for PR-2 spectral graph diagnostics.

Status: [D] purely for software verification.
"""

import json
from pathlib import Path

def write_report():
    data_file = Path("verification/data/pregeometry/pr2/pr2_spectral_diagnostics.json")
    if not data_file.exists():
        print("Data file not found. Run experiments/run_pr2_spectral_diagnostics.py first.")
        return
        
    with open(data_file, "r") as f:
        data = json.load(f)
        
    report_lines = [
        "# PR-2 Spectral Graph Diagnostics Report",
        "",
        "> **Disclaimer:** The PR-2 diagnostic differs from selected null ensembles under the registered software metric. All spectral quantities are exclusively graph diagnostics [D] and carry no physical interpretation.",
        "",
        "## Configuration",
        f"- **Iterations:** {data['metadata']['iterations']}",
        f"- **Seed:** {data['metadata']['seed']}",
        f"- **Walk Length:** {data['metadata']['max_walk_length']}",
        "",
        "## PR-0 Toy Graph Diagnostics",
        f"- **Spectral Gap:** {data['pr0_toy_graph']['spectral_gap']:.6f}",
        f"- **Log-Slope (Window 5-15):** {data['pr0_toy_graph']['log_slope']:.6f}",
        "",
        "### Random Walk Return Probabilities",
        "```text"
    ]
    
    for i, p in enumerate(data['pr0_toy_graph']['random_walk_return_probs']):
        report_lines.append(f"Step {i+1:2d}: {p:.6f}")
        
    report_lines.append("```")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("Status: [D] - Pure graph diagnostic. No forbidden target labels are present.")
    
    out_dir = Path("verification/data/pregeometry/pr2")
    out_file = out_dir / "pr2_report.md"
    
    with open(out_file, "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"Report written to {out_file}")

if __name__ == "__main__":
    write_report()

"""
PREREG-PR-B1 — Entry Point
============================
Dispatches to the master orchestrator.

Usage:
    python -m prb1 orchestrate --master AG2 [--pilot] [--skip-validation]
    python -m prb1 blinding-check
    python -m prb1 manifest [generate|verify]
    python -m prb1 validate-detector
    python -m prb1 seeds --verify
"""

from __future__ import annotations

import sys


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "PREREG-PR-B1 — Blinded Matrix Condensation Protocol\n"
            "Protocol ID: PREREG-PR-B1-002-AG2\n"
            "Evidence ceiling: [D]\n"
            "\nCommands:\n"
            "  orchestrate    Run the full orchestrated protocol\n"
            "  blinding-check Run the forbidden-pattern scanner\n"
            "  manifest       Generate or verify data-freeze manifest\n"
            "  validate-detector  Run the detector validation gate\n"
            "  seeds          Verify seed determinism\n"
        )
        sys.exit(0)

    command = sys.argv[1]
    remaining = sys.argv[2:]

    if command == "orchestrate":
        from .orchestrator import main as orch_main
        orch_main(remaining)

    elif command == "blinding-check":
        from .blinding_check import main as blinding_main
        blinding_main()

    elif command == "manifest":
        from .manifest import main as manifest_main
        # Forward remaining args
        sys.argv = [sys.argv[0]] + remaining
        manifest_main()

    elif command == "validate-detector":
        from .eval.validation import main as validation_main
        validation_main()

    elif command == "seeds":
        from .sim.seeds import main as seeds_main
        seeds_main()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

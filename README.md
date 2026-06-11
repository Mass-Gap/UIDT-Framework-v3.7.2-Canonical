# Experimental Pregeometry Benchmark Workspace

> **Disclaimer:** This is a separate experimental pregeometry workspace, NOT the canonical UIDT v3.9 repository. Do not claim canonical UIDT v3.9 status. All physical interpretations derived from this workspace remain [D/E].

## Overview
This repository provides a leakage-safe pregeometry harness for exploring graph invariants, null models, and dashboard telemetry. 

## Setup & Installation
1. Install dependencies: `pip install -r requirements.txt`
2. Run the test suite: `py -m pytest verification/tests/ -q -p no:cacheprovider`

## Governance & AI Audit Policy
All agents and contributors must adhere to the rules defined in `AI_AUDIT_POLICY.md` and the `AGENTS.md` steering baseline.
- **Rule:** Do not introduce physical constants, target cosmology values, Standard Model targets, or calibrated UIDT parameters into pregeometry growth rules, null ensembles, dashboards, or diagnostics unless a dedicated reviewed task explicitly requires it.
- **Rule:** Runtime artifacts must only be generated under `verification/data/pregeometry/`.

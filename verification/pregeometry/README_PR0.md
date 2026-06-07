# UIDT PR-0 — Leakage-Proof Pregeometry Harness Skeleton

## Purpose

This package is a minimal, repository-safe starter for a UIDT v4.x pregeometry benchmark harness.
It is intentionally small. It does **not** simulate the universe, does **not** model cosmology,
does **not** derive spacetime, and does **not** derive the Standard Model.

The only PR-0 objective is to establish a reproducible, coordinate-free relational carrier with
fail-fast leakage checks and exact graph invariants.

## Scientific status

| Statement | Status |
|---|---|
| The code computes exact graph invariants for the executed code path. | `[A]` software invariant only |
| The relational carrier is a toy pre-geometric structure. | `[D/E]` |
| The harness establishes physical spacetime emergence. | Not claimed |
| The harness establishes cosmological validity. | Not claimed |
| The harness establishes Standard Model emergence. | Not claimed |
| A failed PR-0 run falsifies UIDT globally. | Not claimed |

## Primary research question

```text
Can a coordinate-free relational carrier with deterministic rewrite rules produce exact,
reproducible graph invariants under a fail-fast target-leakage audit?
```

## Directory layout

```text
verification/
  __init__.py
  pregeometry/
    __init__.py
    README_PR0.md
    CODEX_PR0_MASTER_INSTRUCTIONS.md
    MANIFEST.md
    PRE_REGISTERED_OBSERVABLES.md
    primitives.py
    growth_rules.py
    observables.py
    null_models.py
    leakage_audit.py
    experiments/
      __init__.py
      run_pregeometry_toy.py
    reports/
      __init__.py
      write_pregeometry_report.py
  tests/
    test_pregeometry_pr0.py
  data/
    pregeometry/
      .gitkeep
```

## Reproduction command

From the repository root:

```bash
python -m verification.pregeometry.experiments.run_pregeometry_toy --iterations 8 --seed 39
```

Expected outputs:

```text
verification/data/pregeometry/pr0_run_seed39_iter8.json
verification/pregeometry/reports/pr0_report_seed39_iter8.md
```

## Test command

```bash
python -m pytest verification/tests/test_pregeometry_pr0.py
```

## PR-0 boundaries

Deferred to PR-1 or later:

- spectral dimension
- curvature proxies
- observer-map stability
- null-model separation score
- bootstrap or permutation tests
- any physical interpretation beyond `[D/E]`

## Implementation constraints

- No primitive spatial coordinates.
- No primitive spacetime dimension.
- The unmarked state is absence of carrier structure, not `S(x)=0`.
- Storage structures such as dictionaries, tuples, and adjacency sets are allowed as computation containers only.
- No artifacts are written to repository root.
- Protected project directories are not modified by this starter package.

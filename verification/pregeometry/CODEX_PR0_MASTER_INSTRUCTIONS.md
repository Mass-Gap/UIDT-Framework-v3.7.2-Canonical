# Codex Master Instructions — UIDT PR-0 Pregeometry Harness

## 0. Scope lock

Implement **PR-0 only**.

The target deliverable is a minimal, executable, repository-safe pregeometry benchmark skeleton.
This PR is a software and epistemic infrastructure PR, not a physics-result PR.

## 1. Scientific status

All physical interpretation remains `[D/E]`.
Only exact software invariants for a specific executed code path may be reported as `[A]`.

Correct wording:

```text
The PR-0 run establishes exact reproducibility of selected graph invariants for this code path.
The scientific interpretation of the toy sector remains [D/E].
```

Forbidden wording:

```text
The model simulates the universe.
The model simulates the Big Bang.
The model derives spacetime.
The model derives cosmology.
The model derives the Standard Model.
The model solves dimensional emergence.
The model validates UIDT.
```

## 2. Primary research question

```text
Can a coordinate-free relational carrier with deterministic rewrite rules produce exact,
reproducible graph invariants under a fail-fast target-leakage audit?
```

This question is deliberately narrow.

## 3. Repository placement

Create or modify only:

```text
verification/pregeometry/
verification/tests/
verification/data/pregeometry/
```

Do **not** write generated outputs to repository root.
Do **not** modify:

```text
UIDT-OS/
CANONICAL/
LEDGER/
docs/
releases/
core/
modules/
```

## 4. Required files

Create or preserve the following files:

```text
verification/pregeometry/PRE_REGISTERED_OBSERVABLES.md
verification/pregeometry/primitives.py
verification/pregeometry/growth_rules.py
verification/pregeometry/observables.py
verification/pregeometry/null_models.py
verification/pregeometry/leakage_audit.py
verification/pregeometry/experiments/run_pregeometry_toy.py
verification/pregeometry/reports/write_pregeometry_report.py
verification/tests/test_pregeometry_pr0.py
```

## 5. Ontological implementation rule

The unmarked state is represented as **absence of carrier structure**.

It must not be represented as a scalar field with zero value.

Correct:

```python
RelationalState.unmarked()
```

Incorrect:

```python
S(x) = 0
```

Reason:
A scalar evaluation already assumes a carrier/domain and an evaluation site. The unmarked state has no such carrier.

## 6. Allowed computational storage

The following are allowed as computational data containers:

- dictionaries
- tuples
- sets
- frozen dataclasses
- adjacency relations
- integer identifiers
- deterministic pseudo-random generators for null models

These structures are not physical coordinates.

## 7. Forbidden primitive assumptions

The carrier must not contain:

- primitive spatial coordinates
- primitive spacetime dimension
- primitive background metric
- primitive gauge group
- target cosmological constants
- target observational parameters
- fitted external benchmark values

## 8. PR-0 observables

Compute only exact discrete invariants:

```text
N = number of distinctions
E = number of relations
C = number of connected components
beta_1 = E - N + C
```

No spectral dimension in PR-0.
No curvature proxy in PR-0.
No observer-map stability in PR-0.
No null-model separation score in PR-0.

## 9. Growth-rule requirements

Each deterministic rule must declare or document:

- input invariants
- output invariants
- whether acyclicity is preserved
- whether `beta_1` may change

Required rules:

```text
rule_empty_to_first_distinction
rule_edge_subdivision
rule_triangle_closure
rule_causal_extension_dag_safe
```

A helper function may implement a PR-0 deterministic growth schedule.

## 10. Leakage audit

The audit must fail fast on target-leakage tokens in generation files/configuration files.

The scanner should not scan this instruction document by default, because this document necessarily names the forbidden patterns.

Default scan scope:

```text
verification/pregeometry/growth_rules.py
verification/pregeometry/configs/   if present
```

The audit must return structured results and raise a clear exception on failure.

## 11. Null model policy

PR-0 includes one simple null model only.

Acceptable null models:

- deterministic Erdos-Renyi-style graph using integer thresholds
- deterministic random DAG using integer thresholds

Avoid binary floating-point probability thresholds. Use numerator/denominator integer thresholds.

Example:

```python
rng.randrange(probability_denominator) < probability_numerator
```

## 12. Precision policy

PR-0 should not require floating-point arithmetic.

Do not introduce `mpmath` unless a later proof-critical block requires it.
If it becomes necessary in later PRs, set `mp.dps = 80` locally inside the relevant function or context only.
Do not set global precision.

## 13. Report requirements

The generated report must include:

1. Claims Table
2. Reproduction Note
3. Leakage Audit Result
4. Exact Invariant Table
5. Null-Model Table
6. Negative Results Section
7. Explicit `[D/E]` limitation

Required reproduction command:

```bash
python -m verification.pregeometry.experiments.run_pregeometry_toy --iterations 8 --seed 39
```

## 14. Acceptance criteria

```text
[AC-01] Repository root remains clean.
[AC-02] Protected directories remain unchanged.
[AC-03] Unmarked state has no carrier.
[AC-04] S(x)=0 is not used as initial state.
[AC-05] RelationalState contains no primitive coordinates.
[AC-06] Growth rules are deterministic for fixed seed/config.
[AC-07] beta_1 = E - N + C is computed exactly.
[AC-08] DAG-safe rule preserves acyclicity.
[AC-09] Leakage audit fails on forbidden target tokens in scanned generation files/configs.
[AC-10] Report states that all physical interpretation remains [D/E].
```

## 15. Definition of success

PR-0 succeeds if:

- the command runs deterministically;
- exact invariants are emitted;
- the report is generated;
- tests pass;
- no target leakage is detected in the scanned generation files;
- no root artifacts are produced.

PR-0 does not succeed by producing visually impressive graphs.
PR-0 does not succeed by producing a dimension estimate.
PR-0 does not succeed by matching any physical dataset.

## 16. Definition of failure

PR-0 fails if:

- primitive coordinates appear in `RelationalState`;
- the initial state is represented as scalar zero;
- target physics tokens appear in scanned generation files/configs;
- a DAG-safe rule creates a directed cycle;
- output files are written to root;
- results are non-deterministic for fixed input;
- the report upgrades `[D/E]` interpretation to a physical claim.

## 17. PR-1 deferrals

The following belong to PR-1 or later:

- spectral dimension estimate
- graph diffusion
- curvature proxies
- coarse-graining maps
- observer-map stability
- null-model separation score
- bootstrap intervals
- permutation tests
- literature comparison

Do not implement them in PR-0.

# PRE-REGISTERED OBSERVABLES — UIDT PR-0 Pregeometry Harness

## 1. Status

This file pre-registers the PR-0 observables before any extended model exploration.

All physical interpretation remains `[D/E]`.
Exact graph invariant computation for a fixed executed code path may be reported as `[A]` software reproducibility only.

## 2. Non-claims

PR-0 does not claim:

- universe simulation;
- cosmological modelling;
- spacetime derivation;
- gauge group derivation;
- Standard Model emergence;
- empirical validation of UIDT;
- metric emergence;
- dimensional selection.

## 3. Primary PR-0 research question

```text
Can a coordinate-free relational carrier with deterministic rewrite rules produce exact,
reproducible graph invariants under a fail-fast target-leakage audit?
```

## 4. Registered primary observables

| Symbol | Name | Definition | Status |
|---|---|---|---|
| `N` | distinction count | number of carrier distinctions | `[A]` software invariant |
| `E` | relation count | number of carrier relations | `[A]` software invariant |
| `C` | connected component count | number of connected components in the underlying undirected graph | `[A]` software invariant |
| `beta_1` | cycle rank | `E - N + C` | `[A]` software invariant |

## 5. Registered failure conditions

| ID | Failure condition | Meaning |
|---|---|---|
| `F-01` | Primitive coordinates appear | Carrier is no longer pre-geometric. |
| `F-02` | Initial state is scalar zero | The unmarked state has been misrepresented. |
| `F-03` | Target-leakage token appears in scanned generation files/configs | The model may be importing target structure. |
| `F-04` | DAG-safe rule creates a directed cycle | Causal extension invariant failed. |
| `F-05` | Output artifact written to repository root | Repository hygiene failed. |
| `F-06` | Non-deterministic run for fixed seed/config | Reproducibility failed. |
| `F-07` | Physical interpretation upgraded above `[D/E]` | Evidence discipline failed. |

## 6. Deferred observables

The following are explicitly deferred to PR-1 or later:

| Observable | Reason for deferral |
|---|---|
| spectral dimension | requires diffusion operator and scaling-window registration |
| curvature proxy | requires careful interpretation as graph proxy only |
| observer-map stability | requires multiple coarse-graining maps |
| null-model separation score | requires stable primitives and observable pipeline first |
| bootstrap intervals | requires ensemble protocol |
| permutation tests | requires ensemble protocol |

## 7. Negative result policy

A failed PR-0 run falsifies only the tested toy sector under the registered rules and observables.
It does not falsify UIDT globally.

Correct statement:

```text
Failure to separate from null models in later PRs would falsify only the tested toy sector,
not UIDT as a whole.
```

## 8. Reporting language

The report must use conservative language.

Allowed:

```text
The executed PR-0 code path produced exact graph invariants under the registered rules.
```

Not allowed:

```text
The model derives physical spacetime.
```

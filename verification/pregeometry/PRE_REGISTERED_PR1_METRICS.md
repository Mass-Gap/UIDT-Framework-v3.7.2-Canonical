# PR-1 Pre-Registered Null-Model Metrics

Status: pre-registered software benchmark plan for the separate experimental
pregeometry workspace.

This file registers the PR-1 comparison protocol before the null-ensemble runner
is interpreted. It is not a physical claim and does not describe the canonical
UIDT repository state.

## Scope

PR-1 asks whether the deterministic PR-0 toy trace is distinguishable from a
small set of predeclared graph null ensembles under exact graph-invariant
telemetry.

All physical interpretation remains `[D/E]`. Exact integer invariants may be
reported as `[A]` only for the executed software path. Null-model separation
metrics are `[D]`.

## Primary Observables

The only PR-1 observables are the PR-0 graph-invariant telemetry series:

- `N(t)`
- `E(t)`
- `C(t)`
- `beta_1(t)`

No new physical observable is introduced in PR-1.

## Primary Null Ensembles

The pre-registered null ensembles are:

- Erdos-Renyi graph ensemble
- Random DAG ensemble
- Degree-preserving shuffled graph ensemble
- Preferential-attachment baseline

## Primary Separation Metrics

The pre-registered separation metrics are:

- Final-state L1 distance
- Trajectory L1 distance
- Wasserstein distance for scalar telemetry series
- Permutation test against the selected null ensemble
- Bootstrap confidence interval for ensemble distances

## Failure Conditions

PR-1 must report a negative or inconclusive result if any of the following
conditions occurs:

- The PR-0 toy trace is indistinguishable from all selected null ensembles under
  the registered metrics.
- The sign or ordering of a metric result changes under seed variation.
- Registered forbidden target labels appear in generated dashboard or report
  text.
- A metric is selected after observing the ensemble results.
- Telemetry or report artifacts are written outside the allowed PR-1 paths.

## Claim Boundary

Nonzero separation means distinguishability from the selected null ensembles
under the registered software metrics only. Physical interpretation remains
outside the scope of this benchmark.

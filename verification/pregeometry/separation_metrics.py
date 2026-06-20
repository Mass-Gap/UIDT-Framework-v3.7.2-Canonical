"""Pre-registered PR-1 separation metrics.

Metrics in this module are software comparison metrics with status [D]. They
measure distinguishability from selected null ensembles only.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from verification.pregeometry.dashboard.schemas import assert_no_forbidden_visualization_text
from verification.pregeometry.observables import GraphInvariants
from verification.pregeometry.statistics import (
    bootstrap_confidence_interval,
    fraction_to_jsonable,
    mean_fraction,
)


@dataclass(frozen=True)
class EnsembleMetricSummary:
    ensemble: str
    member_count: int
    final_state_l1_mean: Fraction
    trajectory_l1_mean: Fraction
    wasserstein_mean: Fraction
    permutation_p_value: Fraction
    bootstrap_ci_low: Fraction
    bootstrap_ci_high: Fraction
    claim_status: str = "[D]"
    interpretation_boundary: str = "distinguishability from selected nulls only"

    def as_jsonable(self) -> dict[str, object]:
        return {
            "ensemble": self.ensemble,
            "member_count": self.member_count,
            "final_state_l1_mean": fraction_to_jsonable(self.final_state_l1_mean),
            "trajectory_l1_mean": fraction_to_jsonable(self.trajectory_l1_mean),
            "wasserstein_mean": fraction_to_jsonable(self.wasserstein_mean),
            "permutation_p_value": fraction_to_jsonable(self.permutation_p_value),
            "bootstrap_ci": {
                "low": fraction_to_jsonable(self.bootstrap_ci_low),
                "high": fraction_to_jsonable(self.bootstrap_ci_high),
            },
            "claim_status": self.claim_status,
            "interpretation_boundary": self.interpretation_boundary,
        }


def final_state_l1(reference: GraphInvariants, candidate: GraphInvariants) -> int:
    return _invariant_l1(reference, candidate)


def trajectory_l1(reference: Sequence[GraphInvariants], candidate: Sequence[GraphInvariants]) -> int:
    _require_same_length(reference, candidate)
    return sum(_invariant_l1(left, right) for left, right in zip(reference, candidate))


def wasserstein_distance(reference: Sequence[int], candidate: Sequence[int]) -> Fraction:
    """Return exact 1D Wasserstein distance for equally sized integer samples."""
    _require_same_length(reference, candidate)
    if not reference:
        return Fraction(0, 1)
    left = sorted(reference)
    right = sorted(candidate)
    return sum((abs(a - b) for a, b in zip(left, right)), 0) / Fraction(len(left), 1)


def telemetry_wasserstein(reference: Sequence[GraphInvariants], candidate: Sequence[GraphInvariants]) -> Fraction:
    _require_same_length(reference, candidate)
    n_distance = wasserstein_distance([item.node_count for item in reference], [item.node_count for item in candidate])
    e_distance = wasserstein_distance([item.edge_count for item in reference], [item.edge_count for item in candidate])
    c_distance = wasserstein_distance(
        [item.connected_component_count for item in reference],
        [item.connected_component_count for item in candidate],
    )
    b_distance = wasserstein_distance([item.beta_1 for item in reference], [item.beta_1 for item in candidate])
    return n_distance + e_distance + c_distance + b_distance


def summarize_ensemble_metrics(
    *,
    ensemble_name: str,
    reference_trace: Sequence[GraphInvariants],
    candidate_traces: Sequence[Sequence[GraphInvariants]],
    seed: int,
) -> EnsembleMetricSummary:
    assert_no_forbidden_visualization_text((ensemble_name, "distinguishability from selected nulls only"))
    if not reference_trace:
        raise ValueError("reference_trace must not be empty.")

    final_distances = tuple(final_state_l1(reference_trace[-1], trace[-1]) for trace in candidate_traces)
    trajectory_distances = tuple(trajectory_l1(reference_trace, trace) for trace in candidate_traces)
    wasserstein_distances = tuple(telemetry_wasserstein(reference_trace, trace) for trace in candidate_traces)
    ci_low, ci_high = bootstrap_confidence_interval(trajectory_distances, seed=seed)
    observed = mean_fraction(trajectory_distances)
    pseudo_label_p = pseudo_label_permutation_p_value(reference_trace, candidate_traces)
    return EnsembleMetricSummary(
        ensemble=ensemble_name,
        member_count=len(candidate_traces),
        final_state_l1_mean=mean_fraction(final_distances),
        trajectory_l1_mean=observed,
        wasserstein_mean=mean_fraction(wasserstein_distances),
        permutation_p_value=pseudo_label_p,
        bootstrap_ci_low=ci_low,
        bootstrap_ci_high=ci_high,
    )


def pseudo_label_permutation_p_value(
    reference_trace: Sequence[GraphInvariants],
    candidate_traces: Sequence[Sequence[GraphInvariants]],
) -> Fraction:
    """Return a deterministic pseudo-label permutation diagnostic with status [D]."""
    stats = pseudo_label_statistics(reference_trace, candidate_traces)
    if len(stats) <= 1:
        return Fraction(1, 1)
    observed_stat = stats[0]
    tail_count = sum(1 for stat in stats if stat >= observed_stat)
    return Fraction(tail_count, len(stats))


def pseudo_label_statistics(
    reference_trace: Sequence[GraphInvariants],
    candidate_traces: Sequence[Sequence[GraphInvariants]],
) -> tuple[Fraction, ...]:
    traces = (tuple(reference_trace),) + tuple(tuple(trace) for trace in candidate_traces)
    if len(traces) <= 1:
        return (Fraction(0, 1),)
    return tuple(_mean_distance_to_other_traces(index, traces) for index in range(len(traces)))


def _mean_distance_to_other_traces(
    index: int,
    traces: Sequence[Sequence[GraphInvariants]],
) -> Fraction:
    distances = []
    selected = traces[index]
    for other_index, other in enumerate(traces):
        if other_index == index:
            continue
        distances.append(trajectory_l1(selected, other))
    return mean_fraction(distances)


def _invariant_l1(left: GraphInvariants, right: GraphInvariants) -> int:
    return (
        abs(left.node_count - right.node_count)
        + abs(left.edge_count - right.edge_count)
        + abs(left.connected_component_count - right.connected_component_count)
        + abs(left.beta_1 - right.beta_1)
    )


def _require_same_length(left: Sequence[object], right: Sequence[object]) -> None:
    if len(left) != len(right):
        raise ValueError("Metric inputs must have equal length.")

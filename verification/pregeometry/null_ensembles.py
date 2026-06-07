"""Deterministic PR-1 null ensembles for graph-invariant comparison.

The null ensembles are software baselines only. They do not define growth
semantics for PR-0 and do not carry physical interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Iterable, Sequence

from verification.pregeometry.growth_rules import apply_pr0_growth_step
from verification.pregeometry.observables import GraphInvariants, compute_graph_invariants
from verification.pregeometry.primitives import Relation, RelationalState, state_from_edges


NULL_ENSEMBLE_NAMES = (
    "erdos_renyi",
    "random_dag",
    "degree_preserving_shuffle",
    "preferential_attachment",
)


@dataclass(frozen=True)
class NullTrace:
    """One deterministic null trace member."""

    name: str
    member_index: int
    invariants_by_tick: tuple[GraphInvariants, ...]

    @property
    def final(self) -> GraphInvariants:
        if not self.invariants_by_tick:
            return GraphInvariants(0, 0, 0, 0)
        return self.invariants_by_tick[-1]

    def as_jsonable(self) -> dict[str, object]:
        return {
            "name": self.name,
            "member_index": self.member_index,
            "invariants_by_tick": [item.as_jsonable() for item in self.invariants_by_tick],
        }


def pr0_invariant_trace(iterations: int) -> tuple[GraphInvariants, ...]:
    """Replay PR-0 with existing rules and return the invariant trace."""
    if iterations < 0:
        raise ValueError("iterations must be non-negative.")
    state = RelationalState.unmarked()
    trace = []
    for step in range(iterations):
        result = apply_pr0_growth_step(state, step)
        state = result.state
        trace.append(compute_graph_invariants(state))
    return tuple(trace)


def generate_null_trace(*, name: str, iterations: int, seed: int, member_index: int) -> NullTrace:
    """Generate one deterministic null trace from a pre-registered ensemble."""
    if iterations < 0:
        raise ValueError("iterations must be non-negative.")
    if name not in NULL_ENSEMBLE_NAMES:
        raise ValueError(f"Unknown PR-1 null ensemble: {name}")
    rng = Random(_derived_seed(seed, member_index, name))
    trace: list[GraphInvariants] = []
    reference_edges: tuple[tuple[int, int], ...] = ()
    for tick in range(1, iterations + 1):
        node_count = tick
        if name == "erdos_renyi":
            state = _erdos_renyi_state(node_count, rng)
        elif name == "random_dag":
            state = _random_dag_state(node_count, rng)
        elif name == "degree_preserving_shuffle":
            reference_edges = _reference_path_edges(node_count)
            state = _degree_preserving_shuffle_state(node_count, reference_edges, rng)
        else:
            state = _preferential_attachment_state(node_count, rng)
        trace.append(compute_graph_invariants(state))
    return NullTrace(name=name, member_index=member_index, invariants_by_tick=tuple(trace))


def generate_ensemble(*, name: str, iterations: int, seed: int, ensemble_size: int) -> tuple[NullTrace, ...]:
    if ensemble_size < 0:
        raise ValueError("ensemble_size must be non-negative.")
    return tuple(
        generate_null_trace(name=name, iterations=iterations, seed=seed, member_index=index)
        for index in range(ensemble_size)
    )


def generate_all_ensembles(*, iterations: int, seed: int, ensemble_size: int) -> dict[str, tuple[NullTrace, ...]]:
    return {
        name: generate_ensemble(name=name, iterations=iterations, seed=seed, ensemble_size=ensemble_size)
        for name in NULL_ENSEMBLE_NAMES
    }


def _erdos_renyi_state(node_count: int, rng: Random) -> RelationalState:
    edges = []
    for a in range(node_count):
        for b in range(a + 1, node_count):
            if rng.randrange(max(node_count, 1)) == 0:
                edges.append((a, b))
    return state_from_edges(node_count, edges, directed=False)


def _random_dag_state(node_count: int, rng: Random) -> RelationalState:
    edges = []
    for a in range(node_count):
        for b in range(a + 1, node_count):
            if rng.randrange(max(node_count, 1)) == 0:
                edges.append((a, b))
    return state_from_edges(node_count, edges, directed=True)


def _degree_preserving_shuffle_state(
    node_count: int,
    reference_edges: Sequence[tuple[int, int]],
    rng: Random,
) -> RelationalState:
    if node_count <= 1 or not reference_edges:
        return state_from_edges(node_count, (), directed=False)

    stubs: list[int] = []
    for a, b in reference_edges:
        stubs.extend((a, b))
    rng.shuffle(stubs)

    edges: set[tuple[int, int]] = set()
    leftovers = list(stubs)
    attempts = 0
    while len(leftovers) >= 2 and attempts < len(stubs) * len(stubs):
        attempts += 1
        a = leftovers.pop()
        b = leftovers.pop()
        if a == b:
            leftovers.insert(0, a)
            leftovers.insert(0, b)
            rng.shuffle(leftovers)
            continue
        edge = tuple(sorted((a, b)))
        if edge in edges:
            leftovers.insert(0, a)
            leftovers.insert(0, b)
            rng.shuffle(leftovers)
            continue
        edges.add(edge)

    if len(edges) != len(reference_edges):
        # Deterministic fallback preserves edge count for small simple traces.
        edges = set(reference_edges)
    return state_from_edges(node_count, sorted(edges), directed=False)


def _preferential_attachment_state(node_count: int, rng: Random) -> RelationalState:
    if node_count <= 1:
        return state_from_edges(node_count, (), directed=False)
    edges: list[tuple[int, int]] = [(0, 1)]
    degree = [1, 1] + [0 for _ in range(max(node_count - 2, 0))]
    for new_node in range(2, node_count):
        weighted: list[int] = []
        for existing in range(new_node):
            weighted.extend([existing] * max(degree[existing], 1))
        target = weighted[rng.randrange(len(weighted))]
        edges.append(tuple(sorted((target, new_node))))
        degree[target] += 1
        degree[new_node] += 1
    return state_from_edges(node_count, sorted(set(edges)), directed=False)


def _reference_path_edges(node_count: int) -> tuple[tuple[int, int], ...]:
    return tuple((index, index + 1) for index in range(max(node_count - 1, 0)))


def _derived_seed(seed: int, member_index: int, name: str) -> int:
    name_value = sum((index + 1) * ord(char) for index, char in enumerate(name))
    return seed * 1_000_003 + member_index * 9_176 + name_value


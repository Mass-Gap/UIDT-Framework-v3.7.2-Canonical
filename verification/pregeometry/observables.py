"""Exact PR-0 graph observables.

No floating-point arithmetic is used in this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set

from verification.pregeometry.primitives import DistinctionID, RelationalState


@dataclass(frozen=True)
class GraphInvariants:
    node_count: int
    edge_count: int
    connected_component_count: int
    beta_1: int

    def as_jsonable(self) -> Dict[str, int]:
        return {
            "N": self.node_count,
            "E": self.edge_count,
            "C": self.connected_component_count,
            "beta_1": self.beta_1,
        }


def node_count(state: RelationalState) -> int:
    return state.distinction_count()


def edge_count(state: RelationalState) -> int:
    return state.relation_count()


def connected_component_count(state: RelationalState) -> int:
    """Compute connected components of the underlying undirected graph."""
    if not state.distinctions:
        return 0
    adjacency = state.undirected_adjacency()
    seen: Set[DistinctionID] = set()
    components = 0

    for start in sorted(state.distinctions):
        if start in seen:
            continue
        components += 1
        stack = [start]
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    stack.append(neighbor)
    return components


def beta_1(state: RelationalState) -> int:
    """Return the exact cycle rank beta_1 = E - N + C."""
    n = node_count(state)
    e = edge_count(state)
    c = connected_component_count(state)
    value = e - n + c
    if value < 0:
        raise AssertionError("beta_1 invariant became negative for an undirected carrier view.")
    return value


def compute_graph_invariants(state: RelationalState) -> GraphInvariants:
    n = node_count(state)
    e = edge_count(state)
    c = connected_component_count(state)
    b1 = e - n + c
    if b1 != beta_1(state):
        raise AssertionError("beta_1 consistency check failed.")
    return GraphInvariants(
        node_count=n,
        edge_count=e,
        connected_component_count=c,
        beta_1=b1,
    )

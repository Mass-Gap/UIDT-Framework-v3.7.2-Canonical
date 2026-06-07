"""Deterministic PR-0 null models.

The null models use integer thresholds rather than floating-point probability
comparisons. They are comparison baselines only and carry no physical status.
"""

from __future__ import annotations

import random
from typing import Iterable, Tuple

from verification.pregeometry.primitives import RelationalState, state_from_edges


def erdos_renyi_integer_threshold(
    node_count: int,
    *,
    seed: int,
    probability_numerator: int = 1,
    probability_denominator: int = 3,
) -> RelationalState:
    """Return a deterministic undirected Erdos-Renyi-style graph.

    Edge inclusion uses:
        rng.randrange(probability_denominator) < probability_numerator

    No floating-point thresholds are used.
    """
    _validate_probability(probability_numerator, probability_denominator)
    if node_count < 0:
        raise ValueError("node_count must be non-negative.")
    rng = random.Random(seed)
    edges = []
    for i in range(node_count):
        for j in range(i + 1, node_count):
            if rng.randrange(probability_denominator) < probability_numerator:
                edges.append((i, j))
    return state_from_edges(node_count, edges, directed=False)


def random_dag_integer_threshold(
    node_count: int,
    *,
    seed: int,
    probability_numerator: int = 1,
    probability_denominator: int = 3,
) -> RelationalState:
    """Return a deterministic directed acyclic null graph.

    Edges are allowed only from lower identity token to higher identity token.
    This creates an acyclic orientation by construction.
    """
    _validate_probability(probability_numerator, probability_denominator)
    if node_count < 0:
        raise ValueError("node_count must be non-negative.")
    rng = random.Random(seed)
    edges = []
    for i in range(node_count):
        for j in range(i + 1, node_count):
            if rng.randrange(probability_denominator) < probability_numerator:
                edges.append((i, j))
    return state_from_edges(node_count, edges, directed=True)


def _validate_probability(numerator: int, denominator: int) -> None:
    if not isinstance(numerator, int) or not isinstance(denominator, int):
        raise TypeError("Probability threshold must use integers.")
    if denominator <= 0:
        raise ValueError("probability_denominator must be positive.")
    if numerator < 0:
        raise ValueError("probability_numerator must be non-negative.")
    if numerator > denominator:
        raise ValueError("probability_numerator cannot exceed probability_denominator.")

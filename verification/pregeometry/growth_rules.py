"""Deterministic relational rewrite rules for UIDT PR-0.

These rules operate only on identity-token carrier structure. They do not contain
primitive geometric targets. All physical interpretation remains [D/E].
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from verification.pregeometry.primitives import DistinctionID, Relation, RelationalState


@dataclass(frozen=True)
class RuleMetadata:
    name: str
    preserves_acyclicity: bool
    beta_1_may_change: bool
    input_invariant: str
    output_invariant: str


@dataclass(frozen=True)
class RuleResult:
    state: RelationalState
    metadata: RuleMetadata


EMPTY_TO_FIRST_METADATA = RuleMetadata(
    name="rule_empty_to_first_distinction",
    preserves_acyclicity=True,
    beta_1_may_change=False,
    input_invariant="input carrier is unmarked",
    output_invariant="output carrier has exactly one distinction and no relations",
)

EDGE_SUBDIVISION_METADATA = RuleMetadata(
    name="rule_edge_subdivision",
    preserves_acyclicity=True,
    beta_1_may_change=False,
    input_invariant="input carrier contains at least one relation",
    output_invariant="one relation is replaced by a two-relation path through a new distinction",
)

TRIANGLE_CLOSURE_METADATA = RuleMetadata(
    name="rule_triangle_closure",
    preserves_acyclicity=True,
    beta_1_may_change=True,
    input_invariant="input carrier contains a directed path of length two without shortcut",
    output_invariant="a transitive shortcut relation is added while preserving directed acyclicity",
)

CAUSAL_EXTENSION_METADATA = RuleMetadata(
    name="rule_causal_extension_dag_safe",
    preserves_acyclicity=True,
    beta_1_may_change=False,
    input_invariant="input carrier is either unmarked or directed-acyclic under directed relations",
    output_invariant="a new distinction is appended and, if possible, linked from the previous last distinction",
)


def rule_empty_to_first_distinction(state: RelationalState) -> RuleResult:
    """Create the first distinction from the unmarked carrier."""
    if not state.is_unmarked():
        raise ValueError("rule_empty_to_first_distinction requires an unmarked input state.")
    new_state = state.with_distinction()
    if new_state.distinction_count() != 1 or new_state.relation_count() != 0:
        raise AssertionError("First-distinction rule failed its output invariant.")
    return RuleResult(new_state, EMPTY_TO_FIRST_METADATA)


def rule_causal_extension_dag_safe(state: RelationalState) -> RuleResult:
    """Append one distinction while preserving directed acyclicity."""
    if state.is_unmarked():
        return rule_empty_to_first_distinction(state)
    if not is_directed_acyclic(state):
        raise ValueError("Input state is not directed-acyclic.")

    previous_last = max(state.distinctions, key=lambda d: d.value)
    state_with_new_node = state.with_distinction()
    new_node = max(state_with_new_node.distinctions, key=lambda d: d.value)
    relation = Relation(source=previous_last, target=new_node, directed=True)
    new_state = state_with_new_node.with_relation(relation)
    if not is_directed_acyclic(new_state):
        raise AssertionError("DAG-safe causal extension created a directed cycle.")
    return RuleResult(new_state, CAUSAL_EXTENSION_METADATA)


def rule_triangle_closure(state: RelationalState) -> RuleResult:
    """Add the first available transitive directed shortcut.

    Given relations a->b and b->c, add a->c if absent. This can increase the
    underlying undirected cycle rank while preserving directed acyclicity.
    """
    if not is_directed_acyclic(state):
        raise ValueError("Input state is not directed-acyclic.")

    candidate = _first_transitive_shortcut_candidate(state)
    if candidate is None:
        raise ValueError("No transitive shortcut candidate exists.")
    source, target = candidate
    new_state = state.with_relation(Relation(source=source, target=target, directed=True))
    if not is_directed_acyclic(new_state):
        raise AssertionError("Triangle closure created a directed cycle.")
    return RuleResult(new_state, TRIANGLE_CLOSURE_METADATA)


def rule_edge_subdivision(state: RelationalState) -> RuleResult:
    """Subdivide the lexicographically first relation.

    The selected relation a->b or a--b is replaced by a path a->n->b or a--n--b.
    """
    if not state.relations:
        raise ValueError("rule_edge_subdivision requires at least one relation.")

    selected = sorted(state.relations, key=lambda r: r.canonical_key())[0]
    remaining = tuple(relation for relation in state.relations if relation != selected)
    base = RelationalState(
        distinctions=state.distinctions,
        relations=remaining,
        scalar_labels=state.scalar_labels,
    ).with_distinction()
    new_node = max(base.distinctions, key=lambda d: d.value)
    first = Relation(source=selected.source, target=new_node, directed=selected.directed)
    second = Relation(source=new_node, target=selected.target, directed=selected.directed)
    new_state = base.with_relation(first).with_relation(second)
    if selected.directed and is_directed_acyclic(state) and not is_directed_acyclic(new_state):
        raise AssertionError("Edge subdivision did not preserve directed acyclicity.")
    return RuleResult(new_state, EDGE_SUBDIVISION_METADATA)


def apply_pr0_growth_step(state: RelationalState, step_index: int) -> RuleResult:
    """Apply a deterministic PR-0 growth schedule.

    The schedule is intentionally simple:
    - empty carrier -> first distinction;
    - otherwise try triangle closure every third step when possible;
    - otherwise use DAG-safe causal extension.
    """
    if step_index < 0:
        raise ValueError("step_index must be non-negative.")
    if state.is_unmarked():
        return rule_empty_to_first_distinction(state)
    if step_index % 3 == 2:
        candidate = _first_transitive_shortcut_candidate(state)
        if candidate is not None:
            return rule_triangle_closure(state)
    return rule_causal_extension_dag_safe(state)


def grow_pr0(iterations: int) -> Tuple[RelationalState, Tuple[RuleMetadata, ...]]:
    """Run the deterministic PR-0 growth schedule."""
    if iterations < 0:
        raise ValueError("iterations must be non-negative.")
    state = RelationalState.unmarked()
    metadata = []
    for step in range(iterations):
        result = apply_pr0_growth_step(state, step)
        state = result.state
        metadata.append(result.metadata)
    state.assert_invariants()
    if not is_directed_acyclic(state):
        raise AssertionError("PR-0 growth schedule produced a directed cycle.")
    return state, tuple(metadata)


def is_directed_acyclic(state: RelationalState) -> bool:
    """Return True if the directed part of the carrier is acyclic."""
    adjacency = {distinction: [] for distinction in state.distinctions}
    for relation in state.directed_relations():
        adjacency[relation.source].append(relation.target)

    temporary = set()
    permanent = set()

    def visit(node: DistinctionID) -> bool:
        if node in permanent:
            return True
        if node in temporary:
            return False
        temporary.add(node)
        for target in adjacency[node]:
            if not visit(target):
                return False
        temporary.remove(node)
        permanent.add(node)
        return True

    return all(visit(node) for node in state.distinctions)


def _first_transitive_shortcut_candidate(state: RelationalState) -> Optional[Tuple[DistinctionID, DistinctionID]]:
    directed = sorted(state.directed_relations(), key=lambda r: r.canonical_key())
    outgoing = {distinction: [] for distinction in state.distinctions}
    for relation in directed:
        outgoing[relation.source].append(relation.target)
    for source in sorted(state.distinctions):
        for middle in sorted(outgoing[source]):
            for target in sorted(outgoing[middle]):
                if source == target:
                    continue
                if not state.contains_relation(source, target, directed=True):
                    return source, target
    return None

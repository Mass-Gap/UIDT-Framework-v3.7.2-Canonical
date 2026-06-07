"""Coordinate-free relational primitives for UIDT PR-0.

Scientific status:
    - Exact structural invariants computed on these objects are software-level [A]
      for the executed code path.
    - Any physical interpretation remains [D/E].

Core ontological rule:
    The unmarked state is represented as absence of carrier structure.
    It is not represented as scalar zero.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Iterable, Optional, Tuple


FORBIDDEN_PRIMITIVE_ATTRIBUTE_NAMES = frozenset(
    {
        "coordinate",
        "coordinates",
        "coord",
        "coords",
        "position",
        "positions",
        "spatial",
        "spacetime",
        "dimension",
        "metric",
        "x",
        "y",
        "z",
        "t",
    }
)


@dataclass(frozen=True, order=True)
class DistinctionID:
    """Identifier for a relational distinction.

    The integer value is an identity token and insertion-order label only.
    It is not a spatial coordinate and carries no metric meaning.
    """

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("DistinctionID.value must be an integer identity token.")
        if self.value < 0:
            raise ValueError("DistinctionID.value must be non-negative.")

    def as_str(self) -> str:
        return f"d{self.value}"


@dataclass(frozen=True)
class Relation:
    """Relation between two distinctions.

    The relation may be directed or undirected. Endpoints are identity tokens only.
    Optional integer weights are computational labels, not metric distances.
    """

    source: DistinctionID
    target: DistinctionID
    directed: bool = False
    weight: Optional[int] = None

    def __post_init__(self) -> None:
        if not isinstance(self.source, DistinctionID):
            raise TypeError("Relation.source must be a DistinctionID.")
        if not isinstance(self.target, DistinctionID):
            raise TypeError("Relation.target must be a DistinctionID.")
        if self.source == self.target:
            raise ValueError("Self-relations are not allowed in PR-0.")
        if not isinstance(self.directed, bool):
            raise TypeError("Relation.directed must be bool.")
        if self.weight is not None and not isinstance(self.weight, int):
            raise TypeError("Relation.weight must be None or int in PR-0.")

    def canonical_key(self) -> Tuple[int, int, bool]:
        """Return a canonical key for duplicate detection."""
        a = self.source.value
        b = self.target.value
        if self.directed:
            return (a, b, True)
        lo, hi = sorted((a, b))
        return (lo, hi, False)

    def endpoints_undirected(self) -> FrozenSet[DistinctionID]:
        return frozenset((self.source, self.target))


@dataclass(frozen=True)
class RelationalState:
    """Coordinate-free carrier state.

    The empty carrier represents the unmarked state.
    Scalar labels are allowed only after a carrier exists.
    """

    distinctions: Tuple[DistinctionID, ...] = field(default_factory=tuple)
    relations: Tuple[Relation, ...] = field(default_factory=tuple)
    scalar_labels: Dict[DistinctionID, int] = field(default_factory=dict)

    @classmethod
    def unmarked(cls) -> "RelationalState":
        """Return the unmarked state as absence of carrier structure."""
        return cls()

    def __post_init__(self) -> None:
        object.__setattr__(self, "distinctions", tuple(self.distinctions))
        object.__setattr__(self, "relations", tuple(self.relations))
        object.__setattr__(self, "scalar_labels", dict(self.scalar_labels))
        self.assert_invariants()

    def assert_invariants(self) -> None:
        """Fail fast on PR-0 carrier invariants."""
        self._assert_no_forbidden_instance_attributes()
        self._assert_distinctions_unique()
        self._assert_relations_reference_existing_distinctions()
        self._assert_relations_unique()
        self._assert_scalar_labels_require_carrier()

    def _assert_no_forbidden_instance_attributes(self) -> None:
        names = set(vars(self).keys())
        forbidden = names.intersection(FORBIDDEN_PRIMITIVE_ATTRIBUTE_NAMES)
        if forbidden:
            raise AssertionError(f"Forbidden primitive attribute(s) found: {sorted(forbidden)}")

    def _assert_distinctions_unique(self) -> None:
        if len(set(self.distinctions)) != len(self.distinctions):
            raise AssertionError("Duplicate DistinctionID values are not allowed.")

    def _assert_relations_reference_existing_distinctions(self) -> None:
        known = set(self.distinctions)
        for relation in self.relations:
            if relation.source not in known or relation.target not in known:
                raise AssertionError("Relation references a distinction outside the carrier.")

    def _assert_relations_unique(self) -> None:
        keys = [relation.canonical_key() for relation in self.relations]
        if len(keys) != len(set(keys)):
            raise AssertionError("Duplicate relations are not allowed.")

    def _assert_scalar_labels_require_carrier(self) -> None:
        if self.is_unmarked() and self.scalar_labels:
            raise AssertionError("Scalar labels cannot exist on the unmarked state.")
        known = set(self.distinctions)
        for distinction in self.scalar_labels:
            if distinction not in known:
                raise AssertionError("Scalar label references a distinction outside the carrier.")

    def is_unmarked(self) -> bool:
        return not self.distinctions and not self.relations and not self.scalar_labels

    def has_carrier(self) -> bool:
        return bool(self.distinctions)

    def next_distinction_id(self) -> DistinctionID:
        if not self.distinctions:
            return DistinctionID(0)
        return DistinctionID(max(d.value for d in self.distinctions) + 1)

    def with_distinction(self) -> "RelationalState":
        new_id = self.next_distinction_id()
        return RelationalState(
            distinctions=self.distinctions + (new_id,),
            relations=self.relations,
            scalar_labels=self.scalar_labels,
        )

    def with_relation(self, relation: Relation) -> "RelationalState":
        state = RelationalState(
            distinctions=self.distinctions,
            relations=self.relations + (relation,),
            scalar_labels=self.scalar_labels,
        )
        state.assert_invariants()
        return state

    def contains_relation(self, source: DistinctionID, target: DistinctionID, directed: bool) -> bool:
        candidate = Relation(source=source, target=target, directed=directed)
        key = candidate.canonical_key()
        return any(relation.canonical_key() == key for relation in self.relations)

    def relation_count(self) -> int:
        return len(self.relations)

    def distinction_count(self) -> int:
        return len(self.distinctions)

    def directed_relations(self) -> Tuple[Relation, ...]:
        return tuple(relation for relation in self.relations if relation.directed)

    def undirected_adjacency(self) -> Dict[DistinctionID, FrozenSet[DistinctionID]]:
        mutable = {distinction: set() for distinction in self.distinctions}
        for relation in self.relations:
            mutable[relation.source].add(relation.target)
            mutable[relation.target].add(relation.source)
        return {key: frozenset(value) for key, value in mutable.items()}

    def as_jsonable(self) -> Dict[str, object]:
        return {
            "distinctions": [distinction.value for distinction in self.distinctions],
            "relations": [
                {
                    "source": relation.source.value,
                    "target": relation.target.value,
                    "directed": relation.directed,
                    "weight": relation.weight,
                }
                for relation in self.relations
            ],
            "scalar_labels": {str(key.value): value for key, value in self.scalar_labels.items()},
        }


def state_from_edges(
    node_count: int,
    edges: Iterable[Tuple[int, int]],
    *,
    directed: bool = False,
) -> RelationalState:
    """Construct a RelationalState from integer identity tokens and edge pairs."""
    if node_count < 0:
        raise ValueError("node_count must be non-negative.")
    distinctions = tuple(DistinctionID(i) for i in range(node_count))
    relations = tuple(
        Relation(DistinctionID(a), DistinctionID(b), directed=directed)
        for a, b in edges
    )
    return RelationalState(distinctions=distinctions, relations=relations)

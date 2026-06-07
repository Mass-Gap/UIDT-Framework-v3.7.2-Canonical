from pathlib import Path

import pytest

from verification.pregeometry.experiments.run_pregeometry_toy import ensure_not_repository_root_output, run_pr0
from verification.pregeometry.growth_rules import (
    grow_pr0,
    is_directed_acyclic,
    rule_causal_extension_dag_safe,
    rule_empty_to_first_distinction,
    rule_triangle_closure,
)
from verification.pregeometry.leakage_audit import LeakageAuditError, assert_no_leakage
from verification.pregeometry.observables import beta_1, compute_graph_invariants
from verification.pregeometry.primitives import DistinctionID, Relation, RelationalState, state_from_edges


def test_unmarked_state_has_no_carrier() -> None:
    state = RelationalState.unmarked()
    assert state.is_unmarked()
    assert not state.has_carrier()
    assert state.distinctions == ()
    assert state.relations == ()
    assert state.scalar_labels == {}


def test_scalar_zero_is_not_used_as_unmarked_state() -> None:
    state = RelationalState.unmarked()
    assert state.scalar_labels == {}
    with pytest.raises(AssertionError):
        RelationalState(scalar_labels={DistinctionID(0): 0})


def test_relational_state_contains_no_primitive_coordinates() -> None:
    state = rule_empty_to_first_distinction(RelationalState.unmarked()).state
    forbidden = {"x", "y", "z", "t", "coordinates", "position", "metric", "dimension"}
    assert forbidden.isdisjoint(vars(state).keys())


def test_beta_1_formula_is_exact_for_triangle() -> None:
    state = state_from_edges(3, [(0, 1), (1, 2), (0, 2)], directed=False)
    invariants = compute_graph_invariants(state)
    assert invariants.node_count == 3
    assert invariants.edge_count == 3
    assert invariants.connected_component_count == 1
    assert invariants.beta_1 == 1
    assert beta_1(state) == 1


def test_dag_safe_rule_preserves_acyclicity() -> None:
    state = RelationalState.unmarked()
    for _ in range(5):
        state = rule_causal_extension_dag_safe(state).state
        assert is_directed_acyclic(state)


def test_triangle_closure_preserves_acyclicity_and_changes_beta_1() -> None:
    state, _ = grow_pr0(3)
    before = compute_graph_invariants(state)
    closed = rule_triangle_closure(state).state
    after = compute_graph_invariants(closed)
    assert is_directed_acyclic(closed)
    assert after.beta_1 == before.beta_1 + 1


def test_leakage_audit_fails_on_forbidden_token(tmp_path: Path) -> None:
    bad = tmp_path / "bad_growth_config.py"
    bad.write_text("target = 'Minkowski'\n", encoding="utf-8")
    with pytest.raises(LeakageAuditError):
        assert_no_leakage([bad], project_root=tmp_path)


def test_repository_root_output_is_rejected(tmp_path: Path) -> None:
    root_output = tmp_path / "pr0_run.json"
    with pytest.raises(AssertionError):
        ensure_not_repository_root_output(root_output, project_root=tmp_path)


def test_pr0_run_is_deterministic_and_writes_inside_allowed_tree(tmp_path: Path) -> None:
    project_root = tmp_path
    package_root = project_root / "verification" / "pregeometry"
    package_root.mkdir(parents=True)
    # Default audit scans growth_rules.py if present. Use a clean minimal file.
    (package_root / "growth_rules.py").write_text("# clean generation placeholder\n", encoding="utf-8")

    first = run_pr0(project_root=project_root, iterations=8, seed=39)
    second = run_pr0(project_root=project_root, iterations=8, seed=39)

    assert first["uidt_invariants"] == second["uidt_invariants"]
    assert first["null_invariants"] == second["null_invariants"]
    assert first["leakage_audit_passed"] is True
    assert Path(first["run_json"]).parts[:3] == ("verification", "data", "pregeometry")
    assert Path(first["report"]).parts[:3] == ("verification", "pregeometry", "reports")

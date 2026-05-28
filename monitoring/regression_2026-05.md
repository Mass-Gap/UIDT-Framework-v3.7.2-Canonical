# Regression Suite Execution Report (2026-05)

## Summary
- **Execution Date:** 2026-05-28
- **Total Tests Collected:** 72
- **Passed:** 72
- **Failed:** 0
- **Time:** 1.44s

## Conclusion
The full regression suite (all verification scripts + integration tests) passed successfully. There were no test failures. The integration continues to demonstrate mathematical determinism. The results are fully consistent with the previous baseline.

## Full Output
```
============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-8.2.2, pluggy-1.6.0 -- /home/jules/.pyenv/versions/3.12.13/bin/python
cachedir: .pytest_cache
rootdir: /app/verification
plugins: cov-7.1.0, anyio-4.13.0
collecting ... collected 72 items

tests/test_core_baseline.py::test_banach_convergence PASSED              [  1%]
tests/test_core_baseline.py::test_lipschitz_contraction PASSED           [  2%]
tests/test_core_baseline.py::test_rg_closure PASSED                      [  4%]
tests/test_core_baseline.py::test_canonical_v395_lambda_s PASSED         [  5%]
tests/test_covariant_unification.py::test_covariant_unification_equation_of_state PASSED [  6%]
tests/test_covariant_unification.py::test_covariant_unification_ir_limit PASSED [  8%]
tests/test_geometric_operator.py::TestGeometricOperator::test_apply_zero_mass_gap PASSED [  9%]
tests/test_geometric_operator.py::TestGeometricOperator::test_apply_positive_harmonic_ir PASSED [ 11%]
tests/test_geometric_operator.py::TestGeometricOperator::test_apply_negative_harmonic_uv PASSED [ 12%]
tests/test_geometric_operator.py::TestGeometricOperator::test_constants_integrity PASSED [ 13%]
tests/test_geometric_operator.py::TestGeometricOperatorStress::test_stress_test_censored PASSED [ 15%]
tests/test_geometric_operator.py::TestGeometricOperatorStress::test_stress_test_boundary PASSED [ 16%]
tests/test_geometric_operator.py::TestGeometricOperatorStress::test_stress_test_stable PASSED [ 18%]
tests/test_geometric_operator.py::TestGeometricOperatorStress::test_stress_test_high_precision_boundary PASSED [ 19%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_initialization PASSED [ 20%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_predict_omega_bbb PASSED [ 22%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_predict_tetraquark_cccc PASSED [ 23%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_predict_x17_anomaly PASSED [ 25%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_predict_x2370_resonance PASSED [ 26%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_predict_glueball_tensor PASSED [ 27%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_predict_glueball_pseudoscalar PASSED [ 29%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_generate_report PASSED [ 30%]
tests/test_harmonic_predictions.py::TestHarmonicPredictor::test_check_proton_anchor PASSED [ 31%]
tests/test_l4_gamma_derivation.py::test_rg_constraint PASSED             [ 33%]
tests/test_l4_gamma_derivation.py::test_49_over_3_is_nearest_group_factor PASSED [ 34%]
tests/test_l4_gamma_derivation.py::test_h4_n99_bridge PASSED             [ 36%]
tests/test_l4_gamma_derivation.py::test_b0_c2fund_lower_bound PASSED     [ 37%]
tests/test_l4_gamma_derivation.py::test_l4_status_unchanged PASSED       [ 38%]
tests/test_lattice_topology.py::TestTorsionLattice::test_calculate_vacuum_energy_zero_planck_mass PASSED [ 40%]
tests/test_lattice_topology.py::TestTorsionLattice::test_calculate_vacuum_frequency PASSED [ 41%]
tests/test_lattice_topology.py::TestTorsionLattice::test_check_thermodynamic_limit PASSED [ 43%]
tests/test_math_solvers.py::TestSolveExactCubicV::test_happy_path PASSED [ 44%]
tests/test_math_solvers.py::TestSolveExactCubicV::test_kappa_zero PASSED [ 45%]
tests/test_math_solvers.py::TestSolveExactCubicV::test_lambda_zero PASSED [ 47%]
tests/test_math_solvers.py::TestSolveExactCubicV::test_numerical_stability_small_lambda PASSED [ 48%]
tests/test_modules_language.py::test_modules_are_english_only_heuristic PASSED [ 50%]
tests/test_monte_carlo_summary.py::test_delta_ledger_consistency PASSED  [ 51%]
tests/test_monte_carlo_summary.py::test_gamma_ledger_consistency PASSED  [ 52%]
tests/test_monte_carlo_summary.py::test_delta_hp_precision PASSED        [ 54%]
tests/test_monte_carlo_summary.py::test_gamma_hp_precision PASSED        [ 55%]
tests/test_monte_carlo_summary.py::test_csv_delta_mean PASSED            [ 56%]
tests/test_monte_carlo_summary.py::test_csv_gamma_mean PASSED            [ 58%]
tests/test_monte_carlo_summary.py::test_csv_psi_mean PASSED              [ 59%]
tests/test_monte_carlo_summary.py::test_gamma_psi_correlation PASSED     [ 61%]
tests/test_monte_carlo_summary.py::test_rg_constraint PASSED             [ 62%]
tests/test_monte_carlo_summary.py::test_torsion_kill_switch PASSED       [ 63%]
tests/test_no_float_in_modules.py::test_no_float_or_round_in_module[/app/modules/photonic_isomorphism.py] PASSED [ 65%]
tests/test_no_float_in_modules.py::test_no_float_or_round_in_module[/app/modules/__init__.py] PASSED [ 66%]
tests/test_no_float_in_modules.py::test_no_float_or_round_in_module[/app/modules/harmonic_predictions.py] PASSED [ 68%]
tests/test_no_float_in_modules.py::test_no_float_or_round_in_module[/app/modules/covariant_unification.py] PASSED [ 69%]
tests/test_no_float_in_modules.py::test_no_float_or_round_in_module[/app/modules/geometric_operator.py] PASSED [ 70%]
tests/test_no_float_in_modules.py::test_no_float_or_round_in_module[/app/modules/rt_geodesics.py] PASSED [ 72%]
tests/test_no_float_in_modules.py::test_no_float_or_round_in_module[/app/modules/lattice_topology.py] PASSED [ 73%]
tests/test_photonic_isomorphism.py::TestPhotonicIsomorphism::test_initialization_constants PASSED [ 75%]
tests/test_photonic_isomorphism.py::TestPhotonicIsomorphism::test_metamaterial_index_calculation PASSED [ 76%]
tests/test_photonic_isomorphism.py::TestPhotonicIsomorphism::test_wormhole_transition_prediction PASSED [ 77%]
tests/test_public_docs_compliance.py::test_readme_has_no_invalid_evidence_tags PASSED [ 79%]
tests/test_public_docs_compliance.py::test_readme_has_no_cosmology_closure_language PASSED [ 80%]
tests/test_public_docs_compliance.py::test_readme_delta_is_marked_as_spectral_gap PASSED [ 81%]
tests/test_reference_traceability.py::test_theoretical_notes_desi_reference_is_correct PASSED [ 83%]
tests/test_simulation_compliance.py::test_hmc_scripts_have_seed_argument PASSED [ 84%]
tests/test_simulation_compliance.py::test_su3_taylor_orders_are_at_least_40 PASSED [ 86%]
tests/test_torsion_consistency.py::TestTorsionConsistency::test_lattice_folding_factor PASSED [ 87%]
tests/test_torsion_consistency.py::TestTorsionConsistency::test_torsion_energy_constant PASSED [ 88%]
tests/test_torsion_consistency.py::TestTorsionConsistency::test_vacuum_frequency_derivation PASSED [ 90%]
tests/test_torsion_kill_switch.py::test_torsion_kill_switch_invariant PASSED [ 91%]
tests/test_torsion_kill_switch.py::test_torsion_kill_switch_function PASSED [ 93%]
tests/test_uidt_proof_engine.py::TestUIDTProver::test_initialization_constants PASSED [ 94%]
tests/test_uidt_proof_engine.py::TestUIDTProver::test_contraction_map_determinism PASSED [ 95%]
tests/test_uidt_proof_engine.py::TestUIDTProver::test_mass_gap_convergence PASSED [ 97%]
tests/test_uidt_proof_engine.py::TestUIDTProver::test_interrupted_convergence PASSED [ 98%]
tests/test_uidt_proof_engine.py::TestUIDTProver::test_vacuum_energy_validation PASSED [100%]

============================== 72 passed in 1.44s ==============================
```

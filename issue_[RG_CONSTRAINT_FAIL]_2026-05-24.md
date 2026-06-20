# [RG_CONSTRAINT_FAIL] λ_S approximation detected 2026-05-24

## Offending code snippets
```text
core/rg_closure.py:9:text value 0.417. The residual of the exact relation is identically zero
core/rg_closure.py:24:        # DO NOT replace with rounded float 0.417 — LINTER PROTECTION (Directive v4.1)
verification/results/raumzeit_aggregated_k7.json:3167:      "jump_defect": 0.41763962803025273,
verification/results/raumzeit_aggregated_k7.json:8080:      "iso_defect_surrogate": 0.4174524902700342,
verification/results/raumzeit_aggregated_k7.json:8374:      "iso_defect_surrogate": 0.4174522036375254,
verification/scripts/checks/chk08_numerics.py:16:        "lambda_S":("0.417",   r"(?i)\b(?:lambda_S|λ_S)\b\s*[\=\approx]\s*([\d\.]+)"),
verification/scripts/checks/chk08_numerics.py:24:    LAMBDA  = mp.mpf('0.417')
verification/scripts/checks/chk08_numerics.py:30:        # It's known that 0.001 is the residual for 0.417 and 0.500
verification/scripts/UIDT_Master_Verification.py:156:    x0 = [1.705, 0.500, 0.417]
verification/scripts/fisher_metric_check.py:17:  lambda_S = 0.417 +/- 0.007      [A-]
verification/scripts/rg_flow_analysis.py:7:- Updated canonical values (κ = 0.500, λ_S = 0.417)
verification/scripts/rg_flow_analysis.py:149:        lambda_canonical = 0.417
verification/scripts/rg_flow_analysis.py:186:    t, sol = rg.solve_rg_flow(g0=1.0, kappa0=0.500, lambda0=0.417,
verification/scripts/rg_flow_analysis.py:194:    plt.axhline(y=0.417, color='#10b981', linestyle='--', alpha=0.5,
verification/scripts/rg_flow_analysis.py:195:                label=r'$\lambda_S^* = 0.417$ (canonical)')
verification/scripts/UIDT-3.6.1-Verification.py:127:x0 = [1.705, 0.500, 0.417]
verification/scripts/error_propagation.py:51:    lambda_S_central = 0.417
verification/scripts/UIDT-3.6.1-Verification-visual.py:44:LAMBDA_S   = 0.41766     # Self-Coupling
verification/scripts/verify_rg_fixed_point.py:35:    # NEVER use rounded float 0.417 here - LINTER PROTECTION (rg_closure.py:L24)
verification/scripts/verify_phase3_2loop_rg.py:13:  - lambda_S = 5/12 exact (not 0.417)
verification/tests/test_core_baseline.py:52:    # 1.25 / 3 = 0.416666...
verification/tests/test_math_solvers.py:26:        """Test with canonical parameters (m_S=1.705, kappa=0.500, lambda_S=0.417)"""
verification/tests/test_math_solvers.py:29:        lambda_S = 0.417
verification/tests/test_math_solvers.py:54:        lambda_S = 0.0
verification/tests/test_math_solvers.py:66:        v = solve_exact_cubic_v(1.705, 0.417, 0.0)
docs/guides/verification-guide.md:153:- Stability landscape: Deep minimum at (κ, λ_S) = (0.5, 0.417)
docs/guides/verification-guide.md:218:  λ_S = 0.417 < 1 ✅ PASS
docs/theory/ghost_sector_lagrangian.md:36:with $v = 47.7$ MeV [A] and $\lambda_S = 0.417$ [A].
docs/theory/rg_lambda_exact_fix.md:17:The ledger carried $\lambda_S = 0.417$, which is a rounding of this exact value.
docs/theory/rg_lambda_exact_fix.md:23:| Ledger (λ_S = 0.417) | 1.250000 | 1.251000 | **0.001000** (>1e-14 ❌) |
docs/theory/rg_lambda_exact_fix.md:32:- λ_S = 0.417   (rounded, residual 0.001)
docs/theory/rg_lambda_exact_fix.md:45:**Never use** `mp.mpf('0.417')` in verification scripts after this fix.
docs/theory/rg_lambda_exact_fix.md:67:- `CONSTANTS.md` — Quick-Copy block: λ_S = 5/12 ≈ 0.41667
docs/theory/rg_lambda_exact_fix.md:68:- All verification scripts using `mp.mpf('0.417')`
docs/theory/rg_2loop_beta.md:64:    lam     = mp.mpf('0.417')
docs/theory/rg_2loop_beta.md:86:    # With calibrated κ=0.500, λ_S=0.417: residual = 0.001 < 1e-2
docs/governance/PR_Review_Protocol_v2.0.md:52:| λ_S | 0.417 ± 0.007 | exact match | [A] |
docs/archive/rescue_pr_a3_advisory.md:37:the rounded value 0.417. Contains explicit linter protection comment.
docs/archive/rescue_pr_a3_advisory.md:57:No λ_S = 0.417 found in any audit file.
docs/research/L4_phase3_2loop_rg_correction_2026-04-28.md:14:## 1. Fix: λS = 5/12 (exact) replaces λS = 0.417
docs/research/L4_phase3_2loop_rg_correction_2026-04-28.md:16:Per TKT-20260403-LAMBDA-FIX, `rg_2loop_beta.md` uses `λS = 0.417`
docs/research/L1_L4_L5_nogo_analysis_2026-04-28.md:118:**Problem:** λS = 0.417 (rounded) → |5κ² − 3λS| ≈ 10⁻³ → **[RG_CONSTRAINT_FAIL]**
docs/research/L1_L4_L5_nogo_analysis_2026-04-28.md:128:# = 5/12 = 0.41666...(repeating)
docs/research/TKT-20260416-Phase3-FRG-NLO-gamma.md:81:| λ_S | 5/12 ≈ 0.41667 [A] | marginal (d=4) |
docs/research/chi_top_formula_audit.md:109:- `LAMBDA_S`: Updated from `0.417` to `5 * mp.mpf("0.5")**2 / 3`
docs/audits/su3_gamma_conjecture_audit.md:39:\gamma_{\text{closed}} = \left(\frac{6 \times 1.710^3 \times 0.417}{13 \times 0.500 \times 0.277}\right)^{1/3} \approx 1.908
docs/audits/su3_gamma_conjecture_audit.md:111:\text{RHS} = 3\lambda_S = 3 \times 0.417 = 1.25099999\ldots
docs/audits/su3_gamma_conjecture_audit.md:125:**[RG_CONSTRAINT_FAIL]** — The ledger rounds $\lambda_S = 0.417$, whereas the exact fixed-point value is:
docs/audits/su3_gamma_conjecture_audit.md:131:The deviation $\Delta\lambda_S = 0.41\overline{6} - 0.417 = -3.\overline{3} \times 10^{-4}$ lies **within the ledger uncertainty $\pm 0.007$**, so no physical inconsistency exists.
docs/audits/su3_gamma_conjecture_audit.md:139:     = 0.41666...  (not 0.417)
docs/qa/TKT-20260403-audit-summary.md:42:| $\lambda_S = 0.417$ (rounded) | $\lambda_S = 5\kappa^2/3 = 5/12$ (exact) |
docs/evidence/mcmc_bayesian_calibration.md:15:| $\lambda_S$ | 0.417 | — | RG fixed point [A] |
docs/evidence/mcmc_bayesian_calibration.md:42:def verify_rg_constraint(kappa_val='0.500', lambda_val='0.417'):
docs/evidence/mcmc_bayesian_calibration.md:49:    With κ=0.500 and λ_S=0.417, the residual is 0.001 — within
docs/evidence/first_principles_evidence_audit_append_2026-04-28.md:59:- λS = 0.417 (old, rounded) → **λS = 5/12 = 0.41666... (exact)**
docs/evidence/evidence-classification.md:34:| UIDT-C-006 | **Self-Coupling** λ_S | 0.417 ± 0.007 | Perturbative (< 1) |
docs/evidence/evidence-classification.md:37:| UIDT-C-014 | **Perturbative Stability** | λ_S = 0.417 < 1 | Valid expansion |
```

## Labels
`rg-constraint-fail`, `blocking`, `critical`

## Reference
`docs/theory/rg_lambda_exact_fix.md`

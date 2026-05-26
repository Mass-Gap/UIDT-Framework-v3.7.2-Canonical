# κ (kappa) Disambiguation — Canonical Comment Block for `UIDTv3_6_1_HMC_Real.py`

Insert the following block immediately after the `import` statements in  
`UIDTv3_6_1_HMC_Real.py`, before the first constant definition.

---

```python
# =============================================================================
# SYMBOL DISAMBIGUATION — κ (kappa) in the UIDT ecosystem
# =============================================================================
# Two independent symbols named κ appear in UIDT-related literature.
# CONFLATION IS A CATEGORY-1 ERROR. Read before modifying any κ-related line.
#
#  κ_UIDT  (this file — variable `kappa` throughout)
#          Value : 0.500 ± 0.008  [dimensionless]
#          Role  : Non-minimal gauge-scalar coupling constant in L_UIDT.
#                  Satisfies the RG fixed-point constraint 5κ² = 3λ_S.
#                  See CANONICAL/CONSTANTS.md and UIDT-C-005 / UIDT-C-010.
#
#  κ_HJS   (NOT present in this file)
#          Value : free complex parameter with dimension of action (≡ ℏ)
#          Role  : Deformation parameter in the Hamilton–Jacobi–Schrödinger
#                  (HJS) linearization of classical ensemble dynamics
#                  (Zhang 2026, arXiv:2601.22697). Setting κ_HJS = ℏ recovers
#                  standard QM. The HMC MD-flow in this file is the classical
#                  HJ flow that HJS theory can linearize in principle, but
#                  κ_HJS does NOT appear operationally here. [Evidence B]
#
# Reference : docs/theoretical_foundations.md §4.2
# Claim     : UIDT-C-055 [Evidence A]
# =============================================================================
```

---

> This comment must be preserved in all future versions of `UIDTv3_6_1_HMC_Real.py`  
> and any derivative HMC scripts. Removal requires an explicit PR with justification.

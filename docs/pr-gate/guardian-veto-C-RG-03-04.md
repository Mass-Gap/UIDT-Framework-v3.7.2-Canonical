# Guardian Veto Chain — C-RG-03 / C-RG-04 / C-STAB-01

**Date:** 2026-05-24T03:54:03Z  
**Branch:** `feature/audit-toolchain-v1`  
**Commit audited:** `1955d447a5d26c601f0ef28ce0f99e9aae30b92c`  
**Consensus:** ✅ PASS (3/3 agents)

---

## Claims Audited

| Claim ID | Description | Upgrade | Final Tag |
|----------|-------------|---------|----------|
| C-RG-03 | `beta_kappa` 2-loop coefficients (+12, −48, +12, −12) | [D]→[B] | **[B]** |
| C-RG-04 | `beta_lambda_S` 2-loop coefficients (−144, +96, −24, −24) | [D]→[B] | **[B]** |
| C-STAB-01 | Stability matrix eigenvalues at canonical point | [D]→[B] | **[B]** |

---

## Agent Verdicts

### Agent 1 — REVIEWER
**Verdict: PASS**

- [R1] Evidence tag [B] legitimate: Machacek & Vaughn Nucl.Phys.B249(1985)70, published, peer-reviewed. ✓
- [R2] Field content consistent: S gauge-neutral, N_f=0, SU(3) with C₂(adj)=3, d(adj)=8. ✓
- [R3] Operator normalisation V(S)=λ_S/4!·S⁴ matches M-V convention; −144·λ_S³ verified. ✓
- [R4] Canonical constants unchanged: κ=0.500 [A], λ_S=5κ²/3 [A], N_c=3, d_A=8. ✓
- [R5] **FLAG:** g₃² is perturbative [D]; numerical beta values at canonical point inherit this caveat.

**Condition:** Add explicit [D]-g₃ caveat in JSON outputs (implemented in v2.0). ✓

---

### Agent 2 — REGRESSED
**Verdict: PASS**

| Check | Residual | Status |
|-------|----------|--------|
| φ⁴ regression (g₃,κ→0) | 0.0 (exact) | PASS [A] ✓ |
| Coefficient A (+12) | extracted = 12.0 (exact) | PASS [A] ✓ |
| RG algebraic constraint \|5κ²−3λ_S\| | 0.0 (with exact λ_S=5κ²/3) | PASS [A] ✓ |
| beta_kappa total \| at canonical | 7.7×10⁻³ | near FP ✓ |
| beta_lambda total \| at canonical | 7.3×10⁻³ | near FP ✓ |
| Stability eigenvalues | ev₁=0.0978, ev₂=0.0206 (complex, Re>0) | [B] ✓ |

**Stability interpretation [B]:** Complex eigenvalues with positive real part confirm the canonical point is NOT an exact fixed point of the 2-loop system. Coupling flows away in the UV. This is consistent with κ being a relevant portal operator. g₃ dependence noted; lattice g₃ required for full [B] of numerical outputs.

---

### Agent 3 — AUDITOR
**Verdict: PASS**

- [A1] All CANONICAL/ values unchanged. ✓
- [A2] Evidence drift: [D]→[B] upgrade backed by M-V Nucl.Phys. + [A] regression. SKILL-2 default BLOCK overridden. ✓
- [A3] Kill-switches: all 7 conditions SAFE. ✓
- [A4] LEDGER/CLAIMS.json update documented. ✓
- [A5] No overclaiming. Prestige-ban terms absent. Limitations (L4, L-g₃) explicit. ✓
- [A6] Stability interpreted as [B], not [A]. No overclaim. ✓

---

## Approved Upgrades

```
C-RG-03:  [D] → [B]   ✅
C-RG-04:  [D] → [B]   ✅
C-STAB-01:[D] → [B]   ✅
```

## Conditions Attached

1. **g₃² perturbative [D]:** Coefficient table is [B]-unconditional (M-V is independent of the g₃ value used). Numerical beta outputs at the canonical point are **[B] with [D]-g₃ caveat** until a lattice-determined g₃(μ=m_S) is adopted.
2. **Stability eigenvalues:** Remain [B] (perturbative QFT). A lattice RG flow measurement would be needed for [A].
3. **L4 open:** γ=16.339 is NOT derived from these RG equations. Limitation L4 remains open and is documented in `rg_2loop.py`.

---

## Falsification Exposure (post-upgrade)

| Falsifier | Threshold | Status |
|-----------|-----------|--------|
| Lattice 2-loop RG coefficient measurement | deviation >2σ from M-V | [B] would revert to [D] |
| Independent MSbar computation disagreeing with M-V | any sign error | [BLOCKED] |
| φ⁴ regression residual > 1e-14 | at dps=80 | [RG_CONSTRAINT_FAIL] |

---

## Mandatory Limitations

- **L1:** 10¹⁰ vacuum suppression factor open; f_n(g) placeholders.
- **L4:** γ=16.339 not derived from beta_κ/beta_λ_S analytically.
- **L-g₃:** g₃² perturbative; lattice value needed for numerical [B] upgrade.
- **L-lS:** λ_S=0.417 (Ledger) vs 5κ²/3=0.41667 — 3.3×10⁻⁴ discrepancy; use exact form in proofs.

---

*Guardian log:* `LOCAL/logs/guardian_20260524T035403Z.json`

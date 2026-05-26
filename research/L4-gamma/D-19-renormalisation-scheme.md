# Decision D-19: Renormalisation Scheme for the BMW L4 Programme

**Decision ID:** D-19  
**Status:** ISSUED  
**Date:** 2026-05-27  
**Authority:** PI P. Rietz  
**Scope:** BMW-truncation computation of γ = 16.339 (Limitation L4)  
**Supersedes:** None (new decision)  
**Blocks resolved:** BC-1 in BLOCKED-O-P1.md  

---

## 1. Decision

The renormalisation scheme for the BMW L4 programme is fixed as:

```
Scheme:      MS-bar (modified minimal subtraction)
Matching scale:  μ_match = m_S = 1.705 ± 0.015 GeV  [D]
Regulator:   Wetterich optimised (Litim) regulator
             R_k(q) = Z_k (k² − q²) θ(k² − q²)
UV initial scale:  k_UV = Λ_UIDT  (to be determined via RG matching)
IR target:   k → 0  (physical vacuum)
```

**Rationale:** m_S = 1.705 GeV is the physical scalar pole mass predicted by
UIDT [D], i.e. the scale at which the EFT is anchored and at which the
Banach fixed point Δ* = 1.710 GeV [A-] is reproduced. It is the natural
matching point between the UV (Yang-Mills) and IR (vacuum) regimes of the
functional flow.

---

## 2. Technical Specifications

### 2.1 Renormalisation Conditions

The three renormalisation conditions fixing the scheme at μ = m_S are:

```
(RC-1)  U_k(v)|_{k=0}  = 0                     (vacuum normalisation)
(RC-2)  U''_k(v)|_{k=0} = m²_S = (1.705 GeV)²  (scalar mass condition)
(RC-3)  Z_k(v)|_{k=0}  = 1                     (field normalisation)
```

These three conditions uniquely fix the integration constants of the BMW
flow equations BMW-1, BMW-2, BMW-3 (see BMW-truncation-roadmap.md).

### 2.2 UV Boundary Conditions

At k = k_UV = Λ_UIDT, the initial conditions are set by the classical
UIDT Lagrangian (Axiom 2, Ontology v3.9):

```
U_{k_UV}(φ)  = (1/2)μ²φ² + (λ_S/4!)φ⁴
             with μ² < 0  (symmetry-broken phase)
             λ_S = 5κ²/3 = 5/12  [A]
Z_{k_UV}(φ)  = 1          (canonical normalisation at UV)
F_{k_UV}(φ)  = 1          (canonical gauge kinetic term at UV)
```

### 2.3 Matching to γ

The gamma invariant is evaluated at the IR endpoint:

```
γ = Δ*_{k→0} / sqrt(Z_{k→0}(v) · μ²_ref)
```

where μ_ref = m_S provides the dimensionful reference scale. Under D-19,
the condition Z_{k→0}(v) = 1 (RC-3) simplifies this to:

```
γ = Δ*_{k→0} / m_S  =  1.710 GeV / 1.705 GeV  ≈  1.003  [TENSION ALERT]
```

**Critical remark:** This naive substitution yields γ ≈ 1.003, NOT 16.339.
This confirms that γ is NOT simply the ratio Δ*/m_S — it is the ratio
Δ*/sqrt(K_S) where K_S = ⟨∂_μS ∂^μS⟩_Ω is the kinetic VEV, which is a
non-trivial output of the BMW flow and does NOT equal m²_S.

Specifically:

```
K_S = Z_{k→0}(v) · (v · m_S)  [to be determined by BMW flow]
```

For γ = 16.339 to emerge, the BMW flow must produce:

```
K_S = (Δ*/γ)²  =  (1.710 GeV / 16.339)²  ≈  (0.1047 GeV)²  ≈  0.01096 GeV²
```

This is the **target value** that the BMW computation must reproduce from
the flow of Z_k(v) under the D-19 boundary conditions.

---

## 3. Evidence Classification

| Quantity | Value | Tag | Basis |
|---|---|---|---|
| μ_match | 1.705 GeV | [D] | UIDT scalar mass prediction |
| λ_S UV | 5/12 | [A] | RG fixed-point relation 5κ²=3λ_S |
| κ UV | 0.500 | [A] | Canonical ledger |
| K_S target | 0.01096 GeV² | [D] | Derived from γ=16.339, Δ*=1.710 |
| γ* (BMW output) | 16.339 (target) | [D] | Not yet confirmed |

---

## 4. Governance

- This decision is binding for all BMW-flow computations targeting L4.
- It does NOT modify the canonical γ = 16.339 [A-] value.
- It does NOT modify CLAIMS.json (no evidence promotion occurs here).
- Revision of D-19 requires a new Decision D-N with explicit justification.
- If the BMW flow under D-19 boundary conditions fails to reproduce
  K_S = 0.01096 GeV² within 10%, a [TENSION ALERT] must be filed and
  D-19 may need revision.

---

## 5. Resolves

- **BC-1** in BLOCKED-O-P1.md: renormalisation scheme is now defined.
- **Remaining blocks:** BC-2 (backreaction) and BC-3 (γ operator) remain
  open. See BLOCKED-O-P1.md.

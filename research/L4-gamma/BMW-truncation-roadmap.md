# L4 Resolution Roadmap: BMW-Truncation Approach for γ = 16.339

**Claim ID:** C2 (Ontology v3.9, Table 3)  
**Limitation:** L4 — Gamma Invariant Origin [A-]  
**Evidence status:** [A-] phenomenologically calibrated; target [A] upon completion  
**Date opened:** 2026-05-26  
**Author:** P. Rietz / UIDT Research Programme  

---

## 1. Problem Statement

The canonical value γ = 16.339 [A-] is determined from kinetic-VEV matching:

```
γ ≡ Δ* / sqrt(K_S),    K_S ≡ ⟨∂_μ S(x) ∂^μ S(x)⟩_Ω
```

All perturbative and semi-perturbative derivation attempts within UIDT v3.9 have
failed to reproduce this value from first principles (see UIDT Framework v3.9,
Appendix F, Open Questions 4–5):

| Approach | Result | Discrepancy | Status |
|---|---|---|---|
| Perturbative 1-loop β-function (RG fixed point) | γ* ≈ 55.8 | factor 3.4 too large | [BLOCKED] |
| Schwinger-Dyson gap equation (F.4) | γ ≈ 3.27 | factor 5 too small | [BLOCKED] |
| SU(3) Casimir candidate γ_bare = 49/3 ≈ 16.333 | 0.037% match | algebraic link to K_S missing | [D] |
| Kinematic VEV Pathway A (canonical) | γ = 16.339 | — | [A-] |

The BMW truncation of the Functional Renormalization Group (FRG) is identified
as the methodologically cleanest available approach to a non-perturbative
first-principles derivation of γ.

---

## 2. BMW Truncation: Method Summary

The **Blaizot–Méndez-Galain–Wschebor (BMW) truncation** (Phys. Lett. B 632,
571, 2006; Phys. Rev. Lett. 99, 150601, 2007) extends the Local Potential
Approximation (LPA) of the Wetterich exact RG by retaining the full
momentum dependence of the scalar 2-point function while closing the vertex
hierarchy at the 4-point level.

### 2.1 Wetterich Flow Equation (exact)

The exact flow equation for the effective action Γ_k reads:

```
∂_k Γ_k = (1/2) Tr{ [Γ_k^(2) + R_k]^{-1} ∂_k R_k }
```

where Γ_k^(2) is the Hessian, R_k the IR regulator (Wetterich optimised:
R_k(q) = Z_k (k² − q²) θ(k² − q²)), and the trace runs over momenta,
Lorentz, and colour indices.

### 2.2 BMW Closure Ansatz

The BMW truncation parametrises the flowing effective action as:

```
Γ_k[S, A] = ∫ d⁴x { (1/2) Z_k(S) (∂_μ S)² + U_k(S)
              − (1/4) F_k(S) F^a_μν F^{aμν}
              + (κ̄/Λ_UIDT) S F^a_μν F^{aμν} }
```

The key structural equations for the UIDT sector are:

```
∂_k U_k(φ)   = (flow of scalar potential)    [eq. BMW-1]
∂_k Z_k(φ)   = (flow of wavefunction renorm)  [eq. BMW-2]
∂_k F_k(φ)   = (flow of gauge-scalar mixing)  [eq. BMW-3]
```

### 2.3 Connection to γ

The gamma invariant is related to the BMW flow via:

```
γ_k ≡ Δ*_k / sqrt(Z_k(v_k) · μ²)
```

where v_k is the running VEV (minimum of U_k), Δ*_k the running gap, and
μ the renormalisation scale. The physical γ is the k→0 limit:

```
γ = lim_{k→0} γ_k
```

The flow equation for γ_k follows from BMW-1 and BMW-2:

```
∂_k γ_k = γ_k [ (∂_k Δ*_k)/Δ*_k − (1/2)(∂_k Z_k(v_k))/Z_k(v_k) ]
```

A non-trivial fixed point γ* = 16.339 would be established if this equation
admits a stable fixed point at the physical renormalisation point
μ = m_S = 1.705 GeV with the UIDT canonical parameters κ = 0.500, λ_S = 5/12.

---

## 3. Required Computation Steps

### Step 1 — Vertex Hierarchy to Γ^(4) [PREREQUISITE]

The BMW flow for Z_k requires the 4-point vertex Γ^(4)_k at zero momentum:

```
∂_k Z_k(φ) = (1/(2(2π)⁴)) ∫ d⁴q { ∂_k R_k(q) / [Γ^(2)_k(q,φ) + R_k(q)]²
              × Γ^(4)_k(0,0,q,−q; φ) }
```

For the UIDT Lagrangian this vertex receives contributions from:
- scalar quartic self-interaction: ~ λ_S
- scalar-gauge mixing vertex: ~ (κ̄/Λ_UIDT)² ⟨F²⟩
- gauge-loop corrections to the scalar sector

**Status:** Γ^(4)_k has NOT been derived for the UIDT system. This is the
primary blocking item.

### Step 2 — Renormalisation Scheme Decision [PREREQUISITE]

The BMW flow must be performed in a specified scheme. The natural matching
point for UIDT is:

```
μ_match = m_S = 1.705 ± 0.015 GeV  [D]
```

Rationale: this is the physical scalar mass pole, i.e. the scale at which the
UIDT EFT is anchored. The scheme must be fixed before any numerical integration.

**Governance decision required:** Decision D-19 (pending PI authorisation).

### Step 3 — Numerical Integration of BMW Flow Equations

With Γ^(4)_k known and the scheme fixed, the BMW system BMW-1/2/3 must be
integrated numerically from k = Λ_UIDT (UV) to k = 0 (IR). The fixed-point
analysis then determines γ*.

Expected output:
- Flow trajectory γ_k(k) from UV to IR
- Fixed-point value γ* (or demonstration that no fixed point at 16.339 exists)
- Stability eigenvalues (relevant/irrelevant directions)

### Step 4 — Kill-Switch Assessment

If BMW yields γ* ≠ 16.339 at > 1% deviation:
→ γ remains [A-] (phenomenological), L4 remains open.

If BMW yields γ* = 16.339 within stated uncertainty:
→ Promote γ from [A-] to [A], close L4, update CLAIMS.json.

If BMW yields γ* incompatible with 16.339 at > 3σ:
→ [TENSION ALERT]: requires formal review; may trigger revision of
  the canonical γ value.

---

## 4. Relation to γ_bare = 49/3 Candidate

Independently, the SU(3) Casimir candidate:

```
γ_bare = (2N_c + 1)² / N_c = 49/3 ≈ 16.333  [D]
```

matches γ = 16.339 to 0.037%. The BMW computation provides a test of
whether this algebraic coincidence reflects a genuine structural connection:
if the BMW fixed point converges to γ* = 49/3 from the Casimir sector, the
algebraic and dynamical derivations would be unified.

This is a secondary hypothesis, classified [D] pending the BMW computation.

---

## 5. Evidence Classification Trajectory

```
Current:  γ = 16.339  [A-]  (kinematic VEV matching, L4 open)
Target:   γ = 16.339  [A]   (BMW fixed point confirmed + residual < 1e-14)
Fallback: γ = 16.339  [A-]  (BMW fails to converge → L4 remains open)
```

---

## 6. Blocking Items Summary

| Item | Description | Priority |
|---|---|---|
| B1 | Γ^(4)_k for UIDT not derived | CRITICAL |
| B2 | Renormalisation scheme D-19 not decided | CRITICAL |
| B3 | BMW-flow integration code not written | HIGH |
| B4 | Backreaction κ̄²⟨F²⟩/Λ² > m²_δS — perturbative expansion invalid | HIGH |

**See also:** BLOCKED-O-P1.md in this directory for the related blocking
assessment of the δS one-loop integral.

---

## 7. References

- Blaizot, Méndez-Galain, Wschebor, Phys. Lett. B 632 (2006) 571
- Blaizot, Méndez-Galain, Wschebor, Phys. Rev. Lett. 99 (2007) 150601
- Delamotte, arXiv:cond-mat/0702365 (FRG review)
- Dupuis et al., Phys. Rep. 910 (2021) 1 (comprehensive FRG review)
- UIDT Framework v3.9, Appendix F (DOI: 10.5281/zenodo.17835200)
- UIDT Ontology v3.9, Section 8.1, L4 (DOI: 10.5281/zenodo.20319634)

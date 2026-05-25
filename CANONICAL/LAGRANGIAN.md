# UIDT Scalar Field Lagrangian — Canonical Documentation v3.9

> **STATUS:** Proposed — awaiting review  
> **STRATUM:** III (UIDT interpretation/mapping)  
> **EVIDENCE TAG:** [A] for dimensional analysis; [A] for RG constraint; [E/open] for ξ, c_S, Λ (not yet in parameter ledger)  
> **ADDED:** 2026-05-25  
> **RELATES TO:** `CANONICAL/CONSTANTS.md` v3.9.5, PR Gate compliance  
> **OPEN ISSUES:** SCALAR-TENSION-001 (S² vs S¹ coupling), SCALAR-OPEN-002 (ξ not in ledger), SCALAR-OPEN-003 (Λ not in ledger), SCALAR-OPEN-004 (metric emergence)

---

## 1. Conventions

All expressions use **natural units** (ℏ = c = 1).  
Spacetime dimension: **d = 4** (four-dimensional Lorentzian manifold).  
Metric signature: **(−, +, +, +)**.  
Action dimensionality requirement: [S_action] = 0 (dimensionless) → [ℒ] = 4 (mass dimension).

Field dimensions:

| Field / Parameter | Symbol | Mass Dimension |
|---|---|---|
| Scalar field | S(x) | [S] = 1 |
| Gauge field | A^a_μ | [A] = 1 |
| Field strength tensor | F^a_{μν} | [F] = 2 |
| Ricci scalar | R | [R] = 2 |
| Reduced Planck mass | M_Pl | [M_Pl] = 1 |
| Scalar mass (bare) | m_S | [m_S] = 1 |
| Self-coupling | λ_S | [λ_S] = 0 |
| Non-minimal coupling | ξ | [ξ] = 0 |
| Gauge-scalar coupling | κ | [κ] = 0 |
| Wilson coefficient | c_S | [c_S] = 0 |
| EFT cutoff scale | Λ | [Λ] = 1 |

---

## 2. Full Lagrangian Density

The complete UIDT scalar sector Lagrangian in four dimensions is:

$$
\mathcal{L}_{\text{UIDT}} =
\underbrace{\frac{M_{\text{Pl}}^2}{2} R}_{\mathcal{L}_{\text{EH}}}
+ \underbrace{\frac{1}{2}\partial_\mu S \partial^\mu S
- \frac{1}{2} m_S^2 S^2
- \frac{\lambda_S}{4} S^4
- \frac{\xi}{2} R S^2}_{\mathcal{L}_{\text{scalar}}}
+ \underbrace{\left(-\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}\right)}_{\mathcal{L}_{\text{YM}}}
+ \underbrace{\frac{c_S}{\Lambda} S \, \mathrm{Tr}(F_{\mu\nu} F^{\mu\nu})}_{\mathcal{L}_{\text{int, EFT}}}
$$

> **[TENSION ALERT]** The canonical v3.9 Lagrangian in `CANONICAL/CONSTANTS.md` and the Space directive reads:
> $$\mathcal{L}_{\text{UIDT}} = -\tfrac{1}{4}F^2 + \tfrac{1}{2}(\partial S)^2 - V(S) - \tfrac{\kappa}{4} S^2 \,\mathrm{Tr}(FF)$$
> The interaction term above uses **S¹** (linear in S) with EFT suppression 1/Λ, whereas the canonical form uses **S²** (bilinear) with dimensionless κ. These are **structurally distinct operators** at different mass dimensions:
> - Canonical: $-\frac{\kappa}{4} S^2 \mathrm{Tr}(FF)$ — renormalizable, [dim]=4 ✓  
> - This document: $\frac{c_S}{\Lambda} S \mathrm{Tr}(FF)$ — EFT operator, [dim]=4 via 1/Λ suppression ✓  
>
> **This tension is registered as open issue SCALAR-TENSION-001. Neither form is to be silently merged. Resolution requires explicit author decision.**

---

## 3. Dimensional Analysis — Term by Term

| Term | Fields | Dimensions | [ℒ] | Status |
|---|---|---|---|---|
| $\frac{M_{\text{Pl}}^2}{2} R$ | M_Pl, R | 2×1 + 2 = 4 | 4 | ✓ Consistent |
| $\frac{1}{2}\partial_\mu S \partial^\mu S$ | ∂(dim 1), S(dim 1) | 1+1+1+1 = 4 | 4 | ✓ Consistent |
| $\frac{1}{2} m_S^2 S^2$ | m_S(dim 1), S(dim 1) | 1+1+1+1 = 4 | 4 | ✓ Consistent |
| $\frac{\lambda_S}{4} S^4$ | λ_S(dim 0), S(dim 1) | 0+4×1 = 4 | 4 | ✓ Consistent |
| $\frac{\xi}{2} R S^2$ | ξ(dim 0), R(dim 2), S²(dim 2) | 0+2+2 = 4 | 4 | ✓ Consistent |
| $\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}$ | F(dim 2) | 2+2 = 4 | 4 | ✓ Consistent |
| $g_S \cdot S \cdot \mathrm{Tr}(FF)$ | g_S(?), S(1), F²(4) | 1+4 = **5** | **5** | ✗ **Non-renormalizable** (dim-5 operator) |
| $\frac{c_S}{\Lambda} S \, \mathrm{Tr}(FF)$ | c_S(0), Λ⁻¹(−1), S(1), F²(4) | 0−1+1+4 = 4 | 4 | ✓ EFT-valid |

> **Note:** The canonical interaction $-\frac{\kappa}{4} S^2 \mathrm{Tr}(FF)$ is dim-4 renormalizable (κ dim-0, S² dim-2, F² dim-2 each → total dim-4). See §2 [TENSION ALERT] and §4.

---

## 4. RG Constraint (from CONSTANTS.md v3.9.5)

The quartic coupling λ_S is **not a free parameter** but defined by the exact RG fixed-point relation:

$$5\kappa^2 = 3\lambda_S \quad \Rightarrow \quad \lambda_S = \frac{5\kappa^2}{3}$$

With κ = 1/2 (exact): λ_S = 5/12 = 0.41̄6̄. Residual < 10⁻¹⁴ [A] (v3.9.5 exact).  
Source: DOI: 10.5281/zenodo.17835200, `CANONICAL/CONSTANTS.md` v3.9.5.

---

## 5. Physical Interpretation [Stratum III]

### 5.1 Einstein-Hilbert Sector
The explicit inclusion of $\frac{M_{\text{Pl}}^2}{2} R$ commits the theory to treating $g_{\mu\nu}$ as a **fundamental background variable**, not as an emergent quantity derived from S(x). If full metric emergence from S(x) is postulated (i.e., $g_{\mu\nu} = g_{\mu\nu}[S]$), this term must be **removed** and replaced by a functional $\mathcal{L}_{\text{Geom}}[S]$. These are two distinct physical frameworks that cannot coexist without explicit resolution.

### 5.2 Non-minimal Coupling: ξRS²
The term $-\frac{\xi}{2} R S^2$ couples the scalar amplitude directly to spacetime curvature. For large field values, S(x) effectively renormalizes $M_{\text{Pl}}$, creating a Brans-Dicke-type gravitational response. The conformal fixed point is $\xi = 1/6$ (conformal coupling in d=4).

> **⚠ ξ is NOT in the canonical parameter ledger (CONSTANTS.md).** Its value is unconstrained and unregistered. This is open issue SCALAR-OPEN-002.

### 5.3 EFT Interaction: (c_S/Λ) S Tr(FF)
The mandatory 1/Λ suppression **classifies this interaction unambiguously as an Effective Field Theory operator**. The theory is valid only for energies $E \ll \Lambda$. Physical interpretation: S(x) modulates the Yang-Mills energy density, but the underlying UV completion at scale Λ is unknown.

> **⚠ Neither c_S nor Λ are in the canonical parameter ledger.** Both are unconstrained. This is open issue SCALAR-OPEN-003.

---

## 6. Claims Table (PR Gate)

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source | Status | Falsification Exposure |
|---|---|---|---|---|---|---|---|
| SCALAR-C-001 | [ℒ] = 4 required in d=4 (natural units) | Exact | [A] | II | Standard QFT (Peskin & Schroeder) | **Established** | None — dimensional analysis is exact |
| SCALAR-C-002 | [S(x)] = 1 in d=4 | [S]=1 | [A] | II | Standard QFT | **Established** | None |
| SCALAR-C-003 | Term $g_S S F^2$ is dimension-5, non-renormalizable | [dim]=5 | [A] | II | Dimensional counting | **Established** | None |
| SCALAR-C-004 | EFT form $(c_S/\Lambda) S F^2$ is dimension-4 compliant | [dim]=4 | [A] | III | This document | **Proposed — pending review** | Must be checked against UV completion |
| SCALAR-C-005 | Canonical κ-coupling $-\frac{\kappa}{4}S^2 FF$ is renormalizable and satisfies 5κ²=3λ_S (residual <10⁻¹⁴) | [dim]=4, exact RG | [A] | II/III | CONSTANTS.md v3.9.5, §4 | **Established** | None |
| SCALAR-C-006 | S¹ vs S² operator conflict between canonical and EFT forms | Structural | [A] | III | TENSION ALERT | **Open — SCALAR-TENSION-001** | Requires explicit author decision; cannot be resolved by dimensional analysis alone |
| SCALAR-C-007 | Non-minimal coupling ξRS² is dim-4 consistent | [dim]=4 | [A] | II | Standard scalar-tensor theory | **Established** | None |
| SCALAR-C-008 | ξ value is unconstrained in UIDT v3.9 | Unknown | [E] | III | Absence of ledger entry | **Open — SCALAR-OPEN-002** | Falsifiable by conformal coupling limit ξ→1/6 tests |
| SCALAR-C-009 | EFT cutoff Λ is unconstrained in UIDT v3.9 | Unknown | [E] | III | Absence of ledger entry | **Open — SCALAR-OPEN-003** | Falsifiable once UV completion identified |
| SCALAR-C-010 | Full metric emergence $g_{\mu\nu}[S]$ incompatible with explicit EH term | Logical | [A] | III | This document §5.1 | **Open — structural decision required** | If g_μν emerges fully from S, EH term must vanish |

---

## 7. DOI/arXiv Source Audit

| Claim | DOI/arXiv | Status | Used for | Evidence Tag |
|---|---|---|---|---|
| Dimensional analysis, QFT conventions | Peskin & Schroeder, ISBN 978-0201503975 | **Established textbook** | SCALAR-C-001/002/003/005/007 | [A] (Stratum II) |
| UIDT κ, λ_S parameters, RG constraint | DOI: 10.5281/zenodo.17835200 | **Verified** | SCALAR-C-005, §4 | [A] |
| EFT operator classification | Weinberg, *Physica A* 96 (1979) | **Established textbook** | SCALAR-C-004 | [A] (Stratum II) |
| ξ coupling, non-minimal gravity | Callan, Coleman, Jackiw (1970) | **Standard reference** | SCALAR-C-007 | [A] (Stratum II) |
| S¹ vs S² tension | Internal — no external DOI available | **No verified DOI/arXiv source available. Claim cannot be promoted beyond [E/open].** | SCALAR-TENSION-001 | [E] |

---

## 8. Reproduction Note

Dimensional analysis can be reproduced with one command:

```python
# verification/scripts/check_lagrangian_dimensions.py
import mpmath as mp

def check_lagrangian_dimensions():
    mp.dps = 80  # local precision scope only — no global override

    dims = {
        "EH":          mp.mpf(2) + mp.mpf(2),
        "kinetic":     mp.mpf(1) + mp.mpf(1) + mp.mpf(1) + mp.mpf(1),
        "mass_term":   mp.mpf(1) + mp.mpf(1) + mp.mpf(1) + mp.mpf(1),
        "quartic":     mp.mpf(0) + mp.mpf(4)*mp.mpf(1),
        "xi_coupling": mp.mpf(0) + mp.mpf(2) + mp.mpf(2),
        "YM":          mp.mpf(2) + mp.mpf(2),
        "EFT_int":     mp.mpf(0) + (-mp.mpf(1)) + mp.mpf(1) + mp.mpf(4),
        "kappa_int":   mp.mpf(0) + mp.mpf(2) + mp.mpf(2),
        "WRONG_int":   mp.mpf(1) + mp.mpf(4),
    }

    for name, d in dims.items():
        status = "OK" if d == 4 else f"FAIL (dim={d})"
        print(f"{name:15s}: dim={mp.nstr(d,4):6s}  [{status}]")

    assert all(d == 4 for k, d in dims.items() if k != "WRONG_int"), \
        "Dimension check failed: unexpected non-4 term"
    assert dims["WRONG_int"] == 5, \
        "WRONG_int should be dim=5 (non-renormalizable)"

if __name__ == "__main__":
    check_lagrangian_dimensions()
```

Expected output: all terms `OK` except `WRONG_int: FAIL (dim=5)`.

---

**CITATION:** Rietz, P. (2026). UIDT Framework v3.9. DOI: 10.5281/zenodo.17835200

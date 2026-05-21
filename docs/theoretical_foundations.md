# UIDT Framework v3.9 — Theoretical Foundations

> **Document status:** Phase 1 draft — 2026-05-21  
> **Branch:** `docs/phase1-hjs-foundations-claims-update`  
> **DO NOT MERGE** without explicit author approval.

---

## 1. Introduction

This document collects the theoretical underpinnings of the UIDT Framework v3.9 Canonical. It serves as the primary reference for conceptual claims registered in `LEDGER/CLAIMS.json` and for reviewer-facing justifications in manuscript submissions.

Section 4 (below) is new as of Phase 1 (May 2026) and addresses the structural connection between the Hamilton–Jacobi–Schrödinger (HJS) linearization (Zhang 2026) and the UIDT Hamiltonian Monte Carlo sampler.

---

## 2. The UIDT Lagrangian

The canonical UIDT v3.9 Lagrangian is

$$
\mathcal{L}_{\text{UIDT}} = -\tfrac{1}{4}F^2 + \tfrac{1}{2}(\partial S)^2 - V(S) - \tfrac{\kappa_{\text{UIDT}}}{4} S^2 \operatorname{Tr}(FF)
$$

with immutable parameters from `CANONICAL/CONSTANTS.md`:

| Symbol | Value | Evidence |
|---|---|---|
| Δ / Δ\* | 1.710 ± 0.015 GeV | [A/B] |
| γ | 16.339 | [A−] |
| **κ\_UIDT** | **0.500 ± 0.008** | **[A]** |
| λ\_S | 0.417 ± 0.007 | [A] |
| v | 47.7 ± 0.5 MeV | [A] |

See `LEDGER/CLAIMS.json` UIDT-C-001 through UIDT-C-010 for full evidence chain.

---

## 3. RG Fixed-Point Constraint

The RG constraint

$$
5\kappa_{\text{UIDT}}^2 = 3\lambda_S = 1.250
$$

must hold with residual $< 10^{-14}$. Violation triggers `[RG_CONSTRAINT_FAIL]`. See UIDT-C-010, UIDT-C-024. [Evidence A]

---

## 4. Structural Connection: HJS Linearization and the UIDT-HMC Sampler

### 4.1 Overview

The Hamiltonian Monte Carlo (HMC) sampler in `UIDTv3_6_1_HMC_Real.py` uses classical Hamiltonian mechanics to generate proposals in the Yang–Mills field configuration space. The Omelyan leapfrog integrator propagates fictitious molecular-dynamics (MD) trajectories on the energy surface defined by the Euclidean lattice action $S[U]$.

Zhang (2026) demonstrates that any classical HJ ensemble — including the pair $(\rho, S)$ describing this MD flow — admits a **unique** minimal complex embedding

$$
\psi = R\, e^{iS/\kappa_{\text{HJS}}}
$$

which satisfies a linear Schrödinger-type equation:

$$
i\kappa_{\text{HJS}}\, \partial_t \psi = -\frac{\kappa_{\text{HJS}}^2}{2m}\nabla^2\psi + V\psi
$$

This linearization is a **representation theorem**, not a quantization step: the variables $(R, S)$ retain their classical meaning; $\psi$ is an auxiliary object that packages their coupled evolution into a linear PDE. [Evidence A — ref. 1]

### 4.2 Symbol Disambiguation — κ\_UIDT ≠ κ\_HJS

> **CRITICAL:** Two symbols named κ appear in the UIDT ecosystem. They are dimensionally and conceptually distinct. Conflation is a Category-1 error.

| Symbol | Value | Dimension | Role | Evidence |
|---|---|---|---|---|
| `κ_UIDT` (≡ `kappa` in code) | 0.500 ± 0.008 | dimensionless | Non-minimal gauge-scalar coupling in $\mathcal{L}_{\text{UIDT}}$; satisfies $5\kappa^2 = 3\lambda_S$ | [A] — UIDT-C-005 |
| `κ_HJS` | free complex parameter | action (= ℏ dimension) | Deformation parameter in HJS linearization; $\kappa_{\text{HJS}} \to \hbar$ in QM limit | [A — ref. 1] |

The HJS parameter $\kappa_{\text{HJS}}$ plays the same structural role as Planck's constant $\hbar$ within the linearized representation. Setting $\kappa_{\text{HJS}} = \hbar$ recovers standard quantum mechanics (Zhang 2026, §Time-reversal symmetry). The UIDT coupling $\kappa_{\text{UIDT}}$ is a dimensionless RG fixed-point value with no direct relation to $\kappa_{\text{HJS}}$. [Evidence A — UIDT-C-055]

The canonical disambiguation comment block for `UIDTv3_6_1_HMC_Real.py` is provided in `docs/kappa_disambiguation_comment.md`.

### 4.3 Structural Correspondence

The HMC trajectory in `UIDTv3_6_1_HMC_Real.py` integrates

$$
\frac{dU}{dt} = \frac{\partial H}{\partial \Pi},\qquad \frac{d\Pi}{dt} = -\frac{\partial H}{\partial U},\qquad H = \frac{\Pi^2}{2} + S[U]
$$

This is precisely the classical HJ flow on the $(\rho, S)$ phase space. The Zhang (2026) HJS theorem guarantees that this flow admits a linear complex representation $\psi[U,t] = R[U,t]\, e^{iS[U,t]/\kappa_{\text{HJS}}}$. The implication is **formal, not operational**: the Omelyan integrator already computes the correct HJ trajectories; the HJS embedding shows that a linear spectral representation of the same trajectories exists in principle. [Evidence B — UIDT-C-054]

This structural correspondence:
- Provides theoretical legitimacy for wave-based and amplitude-inspired analysis of the UIDT vacuum (Stratum III interpretation, Evidence B)
- Does **NOT** alter or replace the Omelyan integration scheme in v3.6.1
- Does **NOT** imply that quantum vacuum structures arise dynamically from classical HMC [Evidence A — UIDT-C-059]

**Limitation L\_HJS-01:** The HJS theorem is proven for finite-dimensional configuration spaces with smooth $(R, S)$. Applicability to the Yang–Mills functional on a lattice (discretized in the code; infinite-dimensional in the continuum limit) is a formal analogy, not a derived result. Category remains [B] pending explicit lattice-HJS compatibility proof.

**Stratum assignment:**
- Stratum I: The UIDT-HMC MD flow equations (classical HJ, implemented in code)
- Stratum II: Zhang (2026) uniqueness and linearization theorem
- Stratum III: Interpretation that HJS legitimizes wave-based vacuum analysis in UIDT

### 4.4 NCF Sampler Outlook (Phase 2 — not yet active)

Park et al. (ICLR 2026) solve optimal transport problems by learning HJ characteristic flows via neural networks, producing closed-form transport maps without numerical integration. A Phase 2 prototype (`feature/ncf-sampler-prototype`) will evaluate whether the NCF architecture can replace the Omelyan leapfrog for UIDT configuration sampling.

**Source audit status:** [AUDIT\_PENDING] — ICLR 2026 acceptance claimed; DOI and camera-ready not independently resolved as of 2026-05-21. See UIDT-C-057.

**Pre-flight conditions** (all five must pass before NCF replaces Omelyan in production):

| # | Condition | Metric |
|---|---|---|
| 1 | Acceptance rate | ≥ 0.70 on UIDT action (cf. Omelyan baseline ~0.75) |
| 2 | Autocorrelation time | τ\_int(γ) < Omelyan τ\_int on identical dataset |
| 3 | RG-residual | \|5κ²−3λ\_S\| < 10⁻¹⁴ end-to-end |
| 4 | γ\_MC mean | within 1σ of 16.374 ± 1.005 on 10k subsample |
| 5 | Independent reproduction | different hardware / seed |

**Critical limitation:** NCF consistency theorems (Park et al. Thm 5.1, 5.4) require quadratic cost on $\mathbb{R}^n$; the UIDT action is non-quadratic on the SU(3) group manifold. Applicability is [Evidence D] — a conjecture pending benchmark. See UIDT-C-056.

### 4.5 Hu et al. 2026 — Algorithmic Inspiration Note

Hu et al. (2026) use precomputed HJ value functions as heuristics for robot path planning. Direct UIDT relevance is low (robotics domain, non-physics action). The algorithmic idea of using precomputed HJ value functions to guide adaptive step-size control in MCMC is noted as [Evidence D] inspiration. Status: [AUDIT\_PENDING] — under peer review as of 2026-05-21. See UIDT-C-058. Do **NOT** cite as physics evidence.

---

## 5. Open Limitations

| ID | Description | Status |
|---|---|---|
| L1 | 10¹⁰ geometric factor derivation | Open [E] — UIDT-C-018 |
| L2 | Electron mass discrepancy ≈23% | Open [E] |
| L4 | γ RG-gap (perturbative RG → γ\* ≈ 55.8 vs canonical 16.339) | Open [E] — UIDT-C-016 |
| L\_HJS-01 | HJS lattice-extension proof | Open [B] — UIDT-C-054 |

---

## References

1. Y. Zhang, "A complex-linear reformulation of Hamilton–Jacobi theory and emergent quantum structure," arXiv:2601.22697v2 [quant-ph] (10 Apr 2026).
2. Park et al., "Neural Hamilton-Jacobi Characteristic Flows for Optimal Transport," ICLR 2026. [AUDIT\_PENDING — DOI unresolved 2026-05-21]
3. Hu et al., "A Hamilton-Jacobi Reachability-Guided Search Framework for Efficient and Safe Indoor Planar Robot Navigation," (2026). [AUDIT\_PENDING — under peer review 2026-05-21]
4. L. D. Landau and E. M. Lifshitz, *Mechanics*. Pergamon Press, 1976.
5. UIDT CANONICAL/CONSTANTS.md v3.9.4 (authoritative parameter source).

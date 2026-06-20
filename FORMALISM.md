# UIDT Formalism v3.9

> **PURPOSE:** Central repository for UIDT equations  
> **RULE:** Math (LaTeX) MUST be separated from interpretation

---

## Lagrangian

### Full UIDT Lagrangian
$$\mathcal{L}_{\text{UIDT}} = \mathcal{L}_{\text{YM}} + \mathcal{L}_S + \mathcal{L}_{\text{int}}$$

### Yang-Mills Sector
$$\mathcal{L}_{\text{YM}} = -\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}$$

### Scalar Sector
$$\mathcal{L}_S = \frac{1}{2} \partial_\mu S \partial^\mu S - V(S)$$

### Scalar Potential
$$V(S) = \frac{\lambda_S}{4} (S^2 - v^2)^2$$

### Interaction (Non-Minimal Coupling)
$$\mathcal{L}_{\text{int}} = -\frac{\kappa}{4} S^2 F^a_{\mu\nu} F^{a\mu\nu}$$

---

## Core Equations

### Vacuum Equation
$$\left\langle S \right\rangle = v = 47.7 \text{ MeV}$$

### Schwinger-Dyson Equation
$$\Box S + \lambda_S S (S^2 - v^2) + \frac{\kappa}{2} S F^2 = 0$$

### Renormalization Group Equation
$$\mu \frac{d\lambda_S}{d\mu} = \beta_{\lambda_S}(\lambda_S, \kappa, g)$$

---

## Fixed-Point Condition

### RG Fixed Point Constraint
$$5\kappa^2 = 3\lambda_S$$

For the canonical exact representation:
$$\kappa=\frac12,\qquad \lambda_S=\frac{5}{12}$$

**Verification:**
$$5 \times (0.500)^2 = 1.250$$
$$3 \times \frac{5}{12} = 1.250$$
$$|5\kappa^2-3\lambda_S| = 0 < 10^{-14} \quad [A]$$

---

## Effective Gap Derivation

### Reduced Algebraic Gap Equation

The reduced effective map is

$$
T(\Delta)=
\sqrt{
m_S^2+
\frac{\kappa^2\mathcal C}{4\Lambda^2}
\left[
1+
\frac{\ln(\Lambda^2/\Delta^2)}{16\pi^2}
\right]
}.
$$

The local Banach fixed-point closure is an [A] statement only inside this one-dimensional reduced model. The projection from the full pure Yang--Mills functional integral to this map remains an open Stratum III assumption [E].

### Spectral Scale

With:
- $\gamma = 16.339$ (kinetic VEV) [A-]
- $\Delta^* = 1.710 \pm 0.015$ GeV [A], internally reduced-model spectral closure
- lattice comparison status [B], not direct particle observation

### Scalar Mass
$$m_S^2 = 2\lambda_S v^2$$
$$m_S = 1.705 \pm 0.015 \text{ GeV} \quad [D]$$

---

## Stability Conditions

### Perturbative Stability
$$\lambda_S < 1 \quad \Rightarrow \quad 0.417 < 1 \checkmark$$

### Vacuum Stability
$$V''(v) = 2\lambda_S v^2 > 0 \quad \Rightarrow \quad 2.907 > 0 \checkmark$$

---

## Cosmological Equations

### Hubble Parameter (Calibrated)
$$H_0 = 70.4 \pm 0.16 \text{ km/s/Mpc}$$

> **Category C:** Calibrated to DESI DR2, NOT derived.

### Vacuum Energy Suppression
$$\rho_{\text{vac}}^{\text{obs}} = \rho_{\text{vac}}^{\text{QFT}} \times \pi^{-2} \times \prod_{n=1}^{99} f_n(g)$$

> **Category C:** Phenomenological 99-step cascade.

### UIDT Wavelength
$$\lambda_{\text{UIDT}} = 0.660 \pm 0.005 \text{ nm}$$

---

## Pillar II-CSF (Covariant Scalar-Field)

### Conformal Density Mapping
$$ \gamma_{CSF} = \frac{1}{2 \sqrt{\pi \ln(\gamma_{UIDT})}} $$

### Planck-Singularity Regularization
$$ \rho_{max} = \Delta^4 \cdot \gamma^{99} $$

### Equation of State (Placeholders)
$$ w_0 = -0.99, \quad w_a = +0.03 $$

> **Strict Caveat:** The CSF extensions are strictly evaluated under Evidence Category `[C]`.  
> They map phenomenologically upon the `[A-]` calibrated lattice invariant $\gamma = 16.339$.  
> **Limitation L4:** $\gamma$ is calibrated, not fundamentally derived.  
> **Limitation L5:** The $N=99$ RG step limit remains empirical.

---

## Casimir Prediction

### Force Anomaly
$$\frac{\Delta F}{F} = +0.59\% \quad \text{at} \quad d = 0.66 \text{ nm}$$

> **Category D:** Unverified prediction.

### Optimal Distance (v3.7.1 corrected)
$$d_{\text{opt}} = 0.854 \text{ nm}$$

---

## Numerical Precision

### Residual Thresholds
| Equation System | Residual | Status |
|-----------------|----------|--------|
| Three-Equation Closure | < 10⁻⁴⁰ | ✅ |
| Branch 1 | 3.2×10⁻¹⁴ | ✅ |
| Branch 2 (excluded) | 1.8×10⁻¹² | ❌ |
| Verification Tolerance | < 10⁻¹⁴ | ✅ |

---

## Constraint Summary

| Constraint | Expression | Value | Status |
|------------|------------|-------|--------|
| RG Fixed Point | 5κ² = 3λ_S | 1.250 = 1.250 | ✅ |
| Perturbative | λ_S < 1 | 0.417 | ✅ |
| Vacuum | V''(v) > 0 | 2.907 | ✅ |
| Gamma | γ kinetic calibration | 16.339 | [A-] |

---

## Reference Implementation

See:
- `docs/theory/effective_gap_derivation.md` — hybrid gap derivation and epistemic boundary
- `verification/scripts/verify_effective_gap_predictions.py` — documentation numerics
- `verification/scripts/UIDT_Master_Verification.py` — legacy master verification runner

---

**CITATION:** Rietz, P. (2026). UIDT v3.9. DOI: 10.5281/zenodo.17835200

# Effective Phenomenological Derivation of the Yang--Mills Scale

**UIDT Framework:** v3.9 Canonical  
**Status:** Active documentation update  
**Evidence posture:** hybrid; no Clay-level proof claim  
**Primary limitation exposure:** L1, L4, L5  
**DOI:** 10.5281/zenodo.17835200

---

## 1. Scope and Epistemic Boundary

This note documents the effective hybrid architecture used for the UIDT Yang--Mills scale. It replaces any reading in which the one-dimensional Banach fixed-point closure is interpreted as a complete constructive proof of pure four-dimensional Yang--Mills existence and mass gap.

The construction separates three logically distinct layers:

| Layer | Content | Evidence | Stratum | Status |
|---|---|---:|---:|---|
| Projection assumption | The non-perturbative infrared sector is represented by an effective scalar information-density field `S(x)`. | [E] | III | open assumption |
| Reduced algebraic fixed point | The projected gap equation defines a local contraction on the algebraic interval. | [A] | III | internal mathematical closure of the reduced model |
| External anchoring | Numerical scale compatibility with lattice/sum-rule inputs and calibrated UIDT constants. | [A-]/[B]/[D] | I/III | calibrated or predictive, not ab-initio proof |

The resulting statement is therefore:

> UIDT v3.9 provides an internally closed, high-precision effective phenomenological derivation of a Yang--Mills scale near `Delta* = 1.710 +/- 0.015 GeV` [A, internal reduced-model closure], with external lattice compatibility [B], but it does not establish the Clay Mathematics Institute problem for pure Yang--Mills theory.

---

## 2. Effective Mean-Field Projection [E]

The hybrid derivation begins from the UIDT Lagrangian sector

```tex
\mathcal{L}_{UIDT}
=-\frac14F^a_{\mu\nu}F^{a\mu\nu}
+\frac12\partial_\mu S\partial^\mu S
-V(S)
-\frac{\kappa}{4}S^2\mathrm{Tr}(FF).
```

with `S(x)` treated as an effective scalar information-density field. In the infrared, the model assumes that the dominant non-perturbative vacuum structure can be represented by a mean-field projection governed by the gluon-condensate input `C`.

This is a modelling assumption. The exact equivalence of this finite mean-field reduction to the full pure Yang--Mills path integral is not established. In particular, the limit removing or decoupling `S(x)` is not assumed to be topologically smooth in the full QFT state space.

---

## 3. Reduced Algebraic Gap Equation [A within the model]

Within the reduced model, define the operator

```tex
T(\Delta)=
\sqrt{
m_S^2+
\frac{\kappa^2\mathcal C}{4\Lambda^2}
\left[
1+
\frac{\ln(\Lambda^2/\Delta^2)}{16\pi^2}
\right]
}.
```

The canonical RG closure condition is

```tex
5\kappa^2=3\lambda_S,
\qquad
|5\kappa^2-3\lambda_S|<10^{-14}.
```

For `kappa = 0.500` [A] and `lambda_S = 5 kappa^2 / 3 = 5/12` [A], the algebraic residual is exactly zero when represented as rational arithmetic. Any numerical implementation must verify this closure using `mpmath.mpf` with `mp.dps = 80` set locally.

The derivative of the reduced operator is

```tex
T'(\Delta)
=
-\frac{\alpha\beta}{\Delta T(\Delta)},
\qquad
\alpha=\frac{\kappa^2\mathcal C}{4\Lambda^2},
\quad
\beta=\frac{1}{16\pi^2}.
```

Near the fixed point, the local Lipschitz constant is

```tex
L\simeq 3.749\times10^{-5}\ll1.
```

Thus the reduced one-dimensional map is a strict local contraction on the chosen algebraic interval. The Banach fixed-point theorem guarantees existence and uniqueness of the fixed point for this reduced system only:

```tex
\Delta^*
=1.710035046742213182020771096614\ldots~\mathrm{GeV}.
```

---

## 4. Calibration and Non-Inflation of Evidence

The scale is not presented as a pure ab-initio prediction from the dimensionless Yang--Mills coupling `g`. It depends on external and UIDT-calibrated inputs.

| Quantity | Value | Evidence | Stratum | Non-inflation note |
|---|---:|---:|---:|---|
| `Delta*` | `1.710 +/- 0.015 GeV` | [A] | III | internal reduced-model spectral closure; not a particle observation |
| `gamma` | `16.339` | [A-] | III | calibrated; not RG-derived |
| `kappa` | `0.500 +/- 0.008` | [A] | III | fixed by UIDT closure |
| `lambda_S` | `5 kappa^2 / 3 ~= 0.4166667` | [A] | III | exact RG relation |
| `C` | model input | [E]/[B-context] | I/III | definition-dependent condensate; must not be treated as universal without source normalization |

The hybrid derivation is valid only if these categories remain explicit. The statement "UIDT proves the Yang--Mills mass gap" must not be used in public repository documentation.

---

## 5. Relation to Pure Yang--Mills and Clay Boundary

The Clay problem requires construction of non-trivial pure Yang--Mills theory on `R^4` with axiomatic rigor and a positive mass gap. The present hybrid UIDT construction does not supply:

1. a construction of the pure Yang--Mills measure on the full infinite-dimensional configuration space;
2. a proof that the `S(x)`-extended theory is continuously deformable to pure Yang--Mills without phase transition or spectral discontinuity;
3. an Osterwalder--Schrader/Wightman reconstruction for the pure theory independent of the effective scalar projection;
4. a derivation of `gamma = 16.339` from first-principles RG flow.

Therefore all Clay-facing files must use "effective derivation", "reduced-model fixed point", "lattice-compatible scale", or "phenomenological model", not "proof", "theorem", or "solution", unless the relevant statement is restricted to the reduced algebraic system.

---

## 6. Falsification Exposure

The hybrid construction remains falsifiable:

| Trigger | Consequence |
|---|---|
| Lattice calculations exclude `Delta* = 1.710 GeV` by `>3 sigma`. | UIDT gap-scale compatibility is falsified. |
| RG closure violates `|5 kappa^2 - 3 lambda_S| < 1e-14`. | [A] algebraic closure fails. |
| `gamma = 16.339` fails in the photonic `n_critical` test. | gamma-sector [A-]/[D] bridge is invalidated. |
| Finite-temperature lattice data show a thermal pattern incompatible with the stated `Delta(T)` ansatz. | Thermal prediction remains or is demoted to [E]. |
| Tensor glueball ratio excludes the UIDT Regge estimate by `>2 sigma` under a documented covariance model. | Glueball-spectrum prediction is falsified. |

---

## 7. Reviewer-Safe Claim Wording

Preferred:

- "The reduced UIDT gap equation admits a unique fixed point under a strong local contraction [A, Stratum III]."
- "The mapping from this reduced model to pure Yang--Mills remains an open physical assumption [E, Stratum III]."
- "The numerical scale is lattice-compatible [B], not experimentally observed as an isolated particle."
- "gamma = 16.339 is calibrated [A-], not presently RG-derived."

Avoid:

- "Clay proof"
- "solves Yang--Mills"
- "unambiguous pure Yang--Mills theorem"
- "direct glueball discovery"
- "thermal mass gap vanishes continuously at Tc" without caveat

---

## 8. Minimal Reproduction

Run:

```bash
python verification/scripts/verify_effective_gap_predictions.py
```

The script verifies the exact RG closure and recomputes the two derived model-level predictions documented in `docs/predictions/`.

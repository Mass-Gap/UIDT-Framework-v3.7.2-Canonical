# UIDT Framework v3.9
## Research Note: Effective Tensor-Glueball Spectrum Prediction

**Status:** Active model prediction  
**Evidence category:** [D]  
**Epistemic stratum:** Stratum III  
**DOI:** 10.5281/zenodo.17835200

---

## 1. Scope

This note records a model-level prediction for the lowest tensor glueball `2++` using the hybrid UIDT gap scale. It is not a lattice result and not a proof of the pure Yang--Mills spectrum. It is a falsifiable phenomenological extrapolation from the reduced UIDT scale `Delta*`.

External lattice literature is used only as a comparison baseline and for source normalization. The prediction itself remains [D].

---

## 2. Inputs

| Input | Value | Evidence | Stratum | Note |
|---|---:|---:|---:|---|
| Scalar spectral scale | `Delta* = 1.710 +/- 0.015 GeV` | [A] | III | internal reduced-model closure |
| String tension scale | `sqrt(sigma) ~= 0.440 GeV` | [B] | I/II | standard lattice scale convention |
| Spin assignment | `J = 2` | [D] | III | effective Regge ansatz |

---

## 3. Effective Regge Ansatz

The model uses the linear trajectory

```tex
m_J^2=(\Delta^*)^2+2\pi\sigma J.
```

For the lowest tensor glueball `J = 2`, with `sigma = (0.440 GeV)^2 = 0.1936 GeV^2`,

```tex
m_{2^{++}}^2
=(1.710)^2+2\pi(0.1936)\cdot2
=5.3569\ldots~\mathrm{GeV}^2,
```

and hence

```tex
m_{2^{++}}^{UIDT-Regge}=2.3145\ldots~\mathrm{GeV}
```

[D]. The corresponding hierarchy is

```tex
m_{2^{++}}/m_{0^{++}}=1.3535\ldots
```

[D].

---

## 4. Comparison Boundary

Lattice SU(3) pure-gauge calculations report the glueball spectrum using Monte Carlo simulations and continuum extrapolations. Morningstar and Peardon investigated glueballs below `4 GeV` in pure-gauge SU(3), including systematic discretization and finite-volume errors, and published the work as Phys. Rev. D 60, 034509. Later SU(N) work by Athenodorou and Teper computed low-lying glueball spectra and string tensions for `N = 2,...,12` with continuum and large-N extrapolations.

The UIDT value must therefore be reported as a model estimate near the conventional lattice tensor-glueball scale, not an independent lattice determination.

---

## 5. Falsification Criterion

The prediction is falsified if future high-precision pure-gauge lattice determinations of `m_2++/m_0++`, with transparent continuum, finite-volume, scale-setting, and covariance treatment, exclude

```tex
m_{2^{++}}/m_{0^{++}}=1.354
```

by more than `2 sigma`.

Agreement with a future calculation would not upgrade the claim to consensus status by itself. The maximum appropriate immediate promotion would be [B] lattice-compatible, subject to independent reproducibility and uncertainty accounting.

---

## 6. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Source | Status | Falsification exposure |
|---|---|---:|---:|---:|---|---|---|
| UIDT-PRED-GB-001 | Effective tensor-glueball mass from UIDT-Regge ansatz | `2.3145 GeV` | [D] | III | this note; verification script | active prediction | lattice tensor sector |
| UIDT-PRED-GB-002 | Tensor/scalar hierarchy | `1.3535` | [D] | III | this note; verification script | active prediction | ratio exclusion `>2 sigma` |
| EXT-LAT-GB-001 | Pure-gauge SU(3) glueball spectrum exists as lattice baseline | qualitative baseline | [B] | I/II | arXiv:hep-lat/9901004; DOI:10.1103/PhysRevD.60.034509 | external baseline | none for UIDT unless used quantitatively |
| EXT-LAT-GB-002 | SU(N) glueball/string-tension continuum study | qualitative baseline | [B] | I/II | arXiv:2106.00364; DOI:10.1007/JHEP12(2021)082 | external baseline | none for UIDT unless used quantitatively |

---

## 7. Verified References

| DOI/arXiv | Status | Used for | Evidence |
|---|---|---|---|
| arXiv:hep-lat/9901004 | resolvable | pure-gauge glueball-spectrum baseline | [B] |
| DOI:10.1103/PhysRevD.60.034509 | resolvable | journal version of Morningstar--Peardon | [B] |
| arXiv:2106.00364 | resolvable | SU(N) glueball/string-tension baseline | [B] |
| DOI:10.1007/JHEP12(2021)082 | resolvable | journal version of Athenodorou--Teper | [B] |

---

## 8. Reproduction Note

```bash
python verification/scripts/verify_effective_gap_predictions.py
```

# UIDT Framework v3.9
## Research Note: Unquenched-QCD Screening Ansatz for the Effective Gap

**Status:** Active model prediction  
**Evidence category:** [D]  
**Epistemic stratum:** Stratum III  
**DOI:** 10.5281/zenodo.17835200

---

## 1. Scope

This note documents a phenomenological unquenched-QCD extension of the hybrid UIDT gap scale. It is a model ansatz for how dynamical fermions could screen the reduced pure-gauge scale `Delta*(0)=1.710 GeV`.

It does not claim a first-principles derivation of full QCD, a physical pion-sector mass gap, or a direct lattice determination of a UIDT mass. In full QCD, light pseudoscalar mesons, operator mixing, and sea-quark effects change the infrared spectrum. The pure-gauge scale must therefore be treated as an effective gluonic-sector anchor, not as the lowest physical excitation of unquenched QCD.

---

## 2. Standard QCD Baseline

The leading-order QCD beta-function coefficient for an `SU(N_c)` gauge theory with `N_f` fundamental fermions is

```tex
\beta_0 = \frac{11}{3}N_c - \frac{2}{3}N_f.
```

For `SU(3)`, this becomes

```tex
\beta_0(N_f) = 11 - \frac{2}{3}N_f
             = \frac{33-2N_f}{3}.
```

Increasing `N_f` reduces the leading asymptotic-freedom coefficient. UIDT uses this fact only as motivation for a phenomenological screening factor.

---

## 3. UIDT Screening Ansatz

Define the unquenched effective gluonic scale by

```tex
\Delta^*(N_f)
=
\Delta^*(0)
\sqrt{\frac{\beta_0(N_f)}{\beta_0(0)}}
=
\Delta^*(0)
\sqrt{\frac{33-2N_f}{33}}.
```

with

```tex
\Delta^*(0)=1.710~\mathrm{GeV}.
```

This is a [D] ansatz. It is not a theorem. It assumes that leading-order beta-function screening can be mapped onto the reduced UIDT gap scale through a square-root response. That square-root response is a model choice and must be tested.

Representative values:

| `N_f` | Interpretation | `Delta*(N_f)` | Evidence | Stratum |
|---:|---|---:|---:|---:|
| 0 | pure Yang--Mills / quenched anchor | `1.7100 GeV` | [A] internal anchor | III |
| 2 | dynamical light `u,d` ansatz | `1.6027 GeV` | [D] | III |
| 3 | dynamical `u,d,s` ansatz | `1.5469 GeV` | [D] | III |
| 2+1 | phenomenological shorthand for light+strange | channel-dependent; use `N_f=3` only as a first proxy | [D] | III |

---

## 4. Chiral Sector Boundary

Dynamical light quarks introduce spontaneous and explicit chiral-symmetry breaking. Pions are pseudo-Nambu--Goldstone bosons associated with approximate chiral symmetry, not direct excitations of the pure Yang--Mills glueball sector.

Therefore:

- the physical infrared spectrum of full QCD is not governed by `Delta*(N_f)` alone;
- the pion mass scale must not be interpreted as the screened glueball scale;
- mixing between gluonic operators and quark bilinears is expected in scalar and pseudoscalar channels;
- the UIDT ansatz applies only to an effective gluonic-sector scale extracted from specified operators and fitting procedures.

---

## 5. Comparison Boundary

Unquenched glueball calculations depend strongly on operator basis, sea-quark masses, lattice spacing, scale setting, and mixing with conventional mesons. Existing lattice studies do not provide a universal single number that can be identified directly with `Delta*(N_f)`.

Consequently, this note defines a future comparison target:

```tex
\Delta^*_{\mathrm{glue-sector}}(N_f=2+1) \approx 1.55~\mathrm{GeV}
```

only after all of the following are specified:

1. the gluonic operator basis;
2. the quark-bilinear operator basis included for mixing;
3. the sea-quark masses and continuum/chiral extrapolation;
4. scale-setting convention;
5. covariance treatment and systematic uncertainty model.

---

## 6. Falsification Criteria

This [D] ansatz is falsified or demoted if matched unquenched lattice simulations show that:

1. the effective gluonic-sector scale does not decrease with increasing active light flavors within uncertainties;
2. an extracted `N_f=2+1` gluonic-sector scale excludes `1.55 GeV` by more than `2 sigma` under a documented covariance model;
3. the square-root beta0 response fails compared with a better-supported scaling law;
4. operator mixing prevents any stable gluonic-sector scale from being defined.

Agreement with one lattice extraction would not promote the claim above [B-context] unless independently reproduced across actions, volumes, operators, and continuum extrapolations.

---

## 7. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Source | Status | Falsification exposure |
|---|---|---:|---:|---:|---|---|---|
| UIDT-PRED-UQCD-001 | Leading beta0 screening ansatz | `Delta*(N_f)=Delta*(0) sqrt((33-2N_f)/33)` | [D] | III | this note | active prediction | unquenched lattice extraction |
| UIDT-PRED-UQCD-002 | `N_f=2` screened scale | `1.6027 GeV` | [D] | III | this note; verification script | active prediction | `N_f=2` gluonic operators |
| UIDT-PRED-UQCD-003 | `N_f=3` screened scale | `1.5469 GeV` | [D] | III | this note; verification script | active prediction | `N_f=2+1` comparison |
| UIDT-PRED-UQCD-004 | Full-QCD physical IR gap | not claimed | [E] | III | this note | blocked | pion/Goldstone sector |
| EXT-UQCD-001 | Leading QCD beta-function coefficient contains `N_f` screening | `beta0=(11/3)Nc-(2/3)Nf` | [B] | II | perturbative QCD literature | external baseline | not a UIDT theorem |
| EXT-UQCD-002 | Unquenched glueball spectra are operator/mixing dependent | qualitative | [B] | I/II | arXiv:1208.1858; arXiv:1702.08174 | external baseline | direct comparison requires matched operators |

---

## 8. Verified References

| DOI/arXiv | Status | Used for | Evidence |
|---|---|---|---|
| arXiv:1701.01404 | resolvable | high-order QCD beta-function context | [B] |
| arXiv:1208.1858 | resolvable | `2+1` unquenched glueball spectrum context | [B] |
| arXiv:1702.08174 | resolvable | `N_f=2` unquenched glueball spectrum and mixing context | [B] |
| arXiv:1406.4987 | resolvable | chiral symmetry breaking / condensate context | [B] |

---

## 9. Reproduction Note

```bash
python verification/scripts/verify_unquenched_qcd_ansatz.py
```

The script verifies the numerical values in this note at local `mp.workdps(80)`. It does not prove the physical validity of the beta0 screening ansatz.

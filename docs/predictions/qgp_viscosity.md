# UIDT Framework v3.9
## Research Note: QGP Shear Viscosity to Entropy Density Ansatz

**Status:** Active model prediction  
**Evidence category:** [D]  
**Epistemic stratum:** Stratum III  
**DOI:** 10.5281/zenodo.17835200

---

## 1. Scope

This note documents a phenomenological UIDT ansatz for the temperature dependence of the shear-viscosity-to-entropy-density ratio, `eta/s`, near the pure-gauge deconfinement scale.

The note is deliberately scoped. It does not claim a first-principles derivation of QGP transport, does not replace hydrodynamic/Bayesian heavy-ion extractions, and does not identify pure SU(3) thermodynamics with full QCD with dynamical quarks.

The claim status is [D]. The full mapping from the reduced UIDT scalar sector to real-time transport coefficients remains an open Stratum III modelling assumption [E/D boundary].

---

## 2. External Baseline

The Kovtun--Son--Starinets result gives the reference scale

```tex
(eta/s)_{KSS} = 1/(4 pi) = 0.079577471545...
```

for a large class of strongly coupled theories with holographic duals. UIDT uses this value as a comparison scale, not as a theorem for QCD or pure Yang--Mills.

Pure SU(3) transport coefficients are difficult lattice observables because shear viscosity is a real-time quantity reconstructed from Euclidean correlators. Meyer reported an estimate `eta/s = 0.134(33)` at `T = 1.65 T_c` in SU(3) gluodynamics under assumptions about the low-frequency spectral function. Heavy-ion extractions in full QCD are model-dependent and typically use Bayesian hydrodynamic inference.

---

## 3. UIDT Thermal Input

The previous thermal UIDT note defines the confined-phase effective gap ansatz

```tex
Delta_eff(T) = Delta(0) sqrt([1 - (T/T_c)^4]_+),
[x]_+ = max(0,x).
```

with `Delta(0)=1.710 GeV` and nominal pure-gauge `T_c = 270 MeV`.

This confined-phase scale is switched off at and above `T_c` by definition of the ansatz. That switch-off does not imply that all high-temperature screening scales vanish.

---

## 4. Phenomenological Transport Ansatz

For `T <= T_c`, define

```tex
eta/s(T) = 1/(4 pi) + K [Delta_eff(T)/T]^alpha,
```

where:

| Parameter | Status | Evidence | Meaning |
|---|---:|---:|---|
| `K > 0` | phenomenological | [D] | strength of the confined-phase transport penalty |
| `alpha > 0` | phenomenological | [D] | scaling exponent for the effective mass penalty |
| `1/(4 pi)` | external reference | [B]/[D-context] | KSS comparison scale, not a QCD theorem |

For `T > T_c`, this confined-phase UIDT ansatz is not used. A high-temperature branch must be supplied separately, e.g. by perturbative QCD, quasiparticle models, or hydrodynamic Bayesian inference. UIDT does not currently predict that branch from first principles.

---

## 5. Consequences

The ansatz has three controlled consequences:

1. **Low-temperature confined regime:** `Delta_eff(T)/T` is large, so `eta/s` is high. This is a model statement about a stiff confined effective medium [D].
2. **Approach to `T_c` from below:** `Delta_eff(T) -> 0`, so the additive UIDT transport penalty vanishes and the ansatz approaches `1/(4 pi)` from above [D].
3. **Above `T_c`:** UIDT does not impose a continuation. The behavior must be matched to an external high-temperature transport model [E/D boundary].

The phrase "exactly reaches the KSS bound" should be avoided unless the sentence is explicitly restricted to this ansatz. A safer wording is:

> In the confined-phase UIDT ansatz, the mass-dependent penalty term vanishes as `T -> T_c^-`, so `eta/s` approaches the KSS reference value from above.

---

## 6. Falsification Criteria

This ansatz is falsified or demoted if any of the following occur:

1. Matched pure-gauge lattice transport reconstructions exclude any positive-parameter representation of the form

```tex
eta/s(T) - 1/(4 pi) = K [Delta_eff(T)/T]^alpha
```

for `T < T_c` within documented uncertainties.

2. The real-time transport channel used for comparison is shown to decouple from the same screening-mass degradation curve that defines `Delta_eff(T)`.

3. Future data require `eta/s < 1/(4 pi)` in the matched pure-gauge channel and the analysis is not attributable to model, reconstruction, or channel mismatch.

Agreement with heavy-ion data alone cannot promote this claim beyond [D]/[B-context] because heavy-ion QGP is full QCD, not pure SU(3).

---

## 7. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Source | Status | Falsification exposure |
|---|---|---:|---:|---:|---|---|---|
| UIDT-PRED-QGP-001 | Confined-phase UIDT viscosity ansatz | `eta/s = 1/(4pi) + K[Delta_eff(T)/T]^alpha` | [D] | III | this note | active prediction | pure-gauge transport reconstructions |
| UIDT-PRED-QGP-002 | KSS-limit approach inside the ansatz | `eta/s -> 1/(4pi)` as `T -> T_c^-` | [D] | III | this note; thermal gap ansatz | active prediction | finite-temperature transport data |
| UIDT-PRED-QGP-003 | Full-QCD heavy-ion transport prediction | not claimed | [E] | III | this note | blocked | requires dynamical-quark extension |
| EXT-QGP-001 | KSS reference scale | `1/(4pi)` | [B]/[D-context] | II | arXiv:hep-th/0405231 | external reference | not a QCD theorem |
| EXT-QGP-002 | SU(3) gluodynamics viscosity baseline | `eta/s = 0.134(33)` at `1.65 T_c` | [B] | I/II | arXiv:0704.1801 | external baseline | spectral reconstruction assumptions |
| EXT-QGP-003 | Full-QCD heavy-ion Bayesian extraction baseline | model-dependent `eta/s(T)` | [B-context] | I/II | Bayesian hydrodynamic literature | external baseline | model dependence |

---

## 8. Verified References

| DOI/arXiv | Status | Used for | Evidence |
|---|---|---|---|
| arXiv:hep-th/0405231 | resolvable | KSS reference value | [B]/[D-context] |
| arXiv:0704.1801 | resolvable | SU(3) gluodynamics viscosity baseline | [B] |
| arXiv:1804.06469 | resolvable | Bayesian full-QCD heavy-ion transport context | [B-context] |
| arXiv:2106.05019 | resolvable | later Bayesian QGP transport context | [B-context] |

---

## 9. Reproduction Note

The thermal input is reproduced by:

```bash
python verification/scripts/verify_effective_gap_predictions.py
```

No new first-principles transport solver is introduced by this note.

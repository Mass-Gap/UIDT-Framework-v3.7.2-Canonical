# UIDT Framework v3.9
## Research Note: Thermal Screening Ansatz for the Effective Gap

**Status:** Active model prediction  
**Evidence category:** [D]  
**Epistemic stratum:** Stratum III  
**DOI:** 10.5281/zenodo.17835200

---

## 1. Scope

This note documents a finite-temperature ansatz for the UIDT effective gap. It must not be read as a first-principles finite-temperature Yang--Mills derivation.

The pure SU(3) deconfinement transition is a thermodynamic transition of the gauge system. The UIDT ansatz below is a phenomenological parameterization of how the reduced zero-temperature gap scale could track an effective condensate-like order parameter below `T_c`. It does not make a statement about all finite-temperature screening scales above `T_c`.

---

## 2. Inputs

| Input | Value | Evidence | Stratum | Note |
|---|---:|---:|---:|---|
| Zero-temperature effective scale | `Delta(0) = 1.710 GeV` | [A] | III | internal reduced-model closure |
| Pure SU(3) critical ratio | `T_c / sqrt(sigma) = 0.629(3)` | [B] | I | lattice thermodynamics |
| Convention scale | `sqrt(sigma) ~= 0.440 GeV` | [B] | I/II | gives `T_c ~= 276.8 MeV` |
| Nominal rounded value | `T_c ~= 270 MeV` | [B] | I/II | common phenomenological convention |

---

## 3. Phenomenological Ansatz

The working ansatz is

```tex
C(T)=C(0) [1 - (T/T_c)^4]_+,
[x]_+ = max(0,x),
```

with

```tex
Delta_eff(T) = Delta(0) sqrt([1 - (T/T_c)^4]_+).
```

This is an effective screening-scale rule [D]. It is not an assertion of critical universality and does not override lattice thermodynamics of the pure-gauge theory.

Representative values using `T_c = 270 MeV`:

| `T` | `T/T_c` | `Delta_eff(T)` | Evidence |
|---:|---:|---:|---:|
| `100 MeV` | `0.37037...` | `1.6938 GeV` | [D] |
| `200 MeV` | `0.74074...` | `1.4296 GeV` | [D] |
| `250 MeV` | `0.92593...` | `0.8802 GeV` | [D] |
| `270 MeV` | `1` | `0` in this ansatz | [D] |

The value `0` at and above `T_c` means that this specific confined-phase effective scale is switched off. It does not characterize every screening scale of the high-temperature phase.

---

## 4. Physics Caveats

1. The ansatz uses a mean-field-like fourth-power suppression and is not a substitute for finite-temperature lattice correlator analysis.
2. Pure SU(3) deconfinement is not to be described as an established continuous second-order melting process in UIDT documentation.
3. Above `T_c`, finite-temperature gauge theory contains nonzero screening scales. The UIDT confined-phase effective gap being set to zero is a modelling convention.
4. Any comparison to lattice data must specify the operator channel, temporal or spatial correlator, renormalization prescription, and scale setting.

---

## 5. Falsification Criterion

The finite-temperature ansatz is falsified or demoted if lattice measurements of the corresponding channel show that the normalized confined-phase screening scale cannot be represented within uncertainties by

```tex
Delta_eff(T)/Delta(0) = sqrt(1 - (T/T_c)^4)
```

for `T < T_c`, after continuum and finite-volume systematics are included.

---

## 6. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Source | Status | Falsification exposure |
|---|---|---:|---:|---:|---|---|---|
| UIDT-PRED-TH-001 | Confined-phase effective thermal gap ansatz | `Delta(0) sqrt([1-(T/T_c)^4]_+)` | [D] | III | this note; verification script | active prediction | finite-temperature lattice correlators |
| UIDT-PRED-TH-002 | `T = 100 MeV` representative value | `1.6938 GeV` | [D] | III | this note; verification script | illustrative | channel-specific lattice data |
| EXT-LAT-TH-001 | Pure SU(3) thermodynamic scale | `T_c / sqrt(sigma) = 0.629(3)` | [B] | I | arXiv:hep-lat/9602007; DOI:10.1016/0550-3213(96)00170-8 | external baseline | none for UIDT unless used quantitatively |

---

## 7. Verified References

| DOI/arXiv | Status | Used for | Evidence |
|---|---|---|---|
| arXiv:hep-lat/9602007 | resolvable | pure SU(3) thermodynamic scale | [B] |
| DOI:10.1016/0550-3213(96)00170-8 | resolvable | journal version of Boyd et al. | [B] |

---

## 8. Reproduction Note

```bash
python verification/scripts/verify_effective_gap_predictions.py
```

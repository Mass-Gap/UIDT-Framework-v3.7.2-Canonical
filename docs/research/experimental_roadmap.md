# Experimental Roadmap — UIDT v3.9

> **Evidence Categories:** [D] Predictions | [B] Lattice compatible  
> **Version:** v3.9 | **Source:** Effective hybrid documentation; Master Report 2 §12–13

## Scope Correction

The Yang--Mills scale is documented as an effective phenomenological derivation. The local Banach contraction is [A] only inside the reduced one-dimensional algebraic model. The projection from this model to pure Yang--Mills remains an open Stratum III assumption [E].

---

## Tier 1 — Near-Term (1–3 Years, 2026–2028)

| Experiment | Observable | UIDT Prediction | Current Sensitivity | Required |
|------------|-----------|----------------|---------------------|----------|
| Lattice QCD (pure gauge) | $0^{++}$ spectral scale | $\Delta^* = 1.710 \pm 0.015$ GeV [A/B-context] | channel-dependent | continuum + finite-volume control |
| Lattice QCD (pure gauge) | $2^{++}/0^{++}$ hierarchy | UIDT-Regge: $1.354$ [D] | channel-dependent | covariance-defined $2\sigma$ test |
| BESIII / PANDA | Glueball candidate phenomenology | comparison only; no direct $\Delta^*$ observation claim | resonance-dependent | mixing analysis |
| LHC Run 3 (ATLAS/CMS) | W/Z boson mass shift | $\delta m_{W/Z} \sim 1.2 \times 10^{-6}$ GeV | ±12 MeV | ±0.1 MeV |
| Cryogenic Resonator | Entropy gradient coupling | $\delta f/f_0 \sim 10^{-18}$ | $10^{-15}$ | $10^{-18}$ |

## Tier 2 — Medium-Term (3–7 Years, 2028–2032)

| Experiment | Observable | UIDT Prediction | Facility |
|------------|-----------|----------------|----------|
| Electron-Ion Collider (EIC) | Gluon polarization structure | Modified $\Delta G$ | BNL |
| FCC-ee (Z-pole) | Z boson mass precision | $\delta m_Z \sim 10^{-4}$ GeV | CERN |
| CMB Spectral Distortions | Information-theoretic corrections | $\delta n_s \sim 0.001$ | PIXIE 2030 |
| Atomic Interferometry | Entropy gradient: $a/g$ | $10^{-12}$ | Various |
| Finite-temperature lattice Yang--Mills | confined-phase screening ansatz | $\Delta(T)=\Delta(0)\sqrt{[1-(T/T_c)^4]_+}$ [D] | lattice collaborations |
| DESI DR3+ | Dark energy EOS $w_a$ | $w_a = +0.03$ (UIDT CSF) [C] | DESI |

## Tier 3 — Long-Term (>7 Years, post-2033)

| Experiment | Observable | UIDT Prediction | Facility |
|------------|-----------|----------------|----------|
| FCC-hh | High-energy glueball-sector production | candidate comparison; not direct proof | CERN |
| Gravitational Wave Detectors | Modified dispersion relations | $\delta v_{\text{GW}}/c \sim 10^{-20}$ | LISA, ET |
| Quantum Gravity Experiments | Information field quantization | QUIDTs | TBD |

## Falsification Criteria

Relevant UIDT sectors are falsified or demoted if **any** of the following hold:

1. Pure-gauge lattice determinations exclude $\Delta^* = 1.710 \pm 0.015$ GeV by more than $3\sigma$ under documented uncertainty construction.
2. No entropy gradient coupling detected at resonator sensitivity $\delta f/f_0 = 10^{-18}$
3. $w_a$ measured as $0.00 \pm 0.005$ (i.e., perfectly consistent with $\Lambda$CDM)
4. RG fixed point $5\kappa^2 = 3\lambda_S$ violated in lattice simulation at $> 3\sigma$

> **Limitation Acknowledgement:** Several Tier 1 predictions require next-generation experimental capabilities not yet available. Current data are compatible with selected UIDT sectors but do not constitute confirmation.

## Cross-References

- `docs/theory/effective_gap_derivation.md` — hybrid gap derivation and Clay boundary
- `docs/predictions/glueball_spectrum.md` — tensor-glueball [D] prediction
- `docs/predictions/thermal_vacuum.md` — finite-temperature [D] ansatz
- `docs/evidence/falsification-criteria.md` — complete falsification matrix
- `FORMALISM.md` — canonical predictions
- `clay-submission/08_Documentation/` — Clay submission experimental section

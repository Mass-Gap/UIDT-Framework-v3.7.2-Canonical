# UIDT Framework v3.9
## Research Note: Tetraquark `T_cc+` Binding-Energy Mapping

**Status:** Active hypothesis  
**Evidence category:** [E] interpretive mapping  
**Epistemic stratum:** Stratum III  
**DOI:** 10.5281/zenodo.17835200

---

## 1. Scope

This note explores whether the UIDT unquenched screening ansatz can be used as an interpretive mapping for the exotic open-charm tetraquark `T_cc+` with valence content `cc ubar dbar`.

The mapping is deliberately classified as [E]. It is not a prediction of the physical `T_cc+` mass from first principles, not a lattice calculation, and not a proof that the UIDT scalar field `S(x)` controls the heavy-light tetraquark potential.

The note is included because `T_cc+` is a useful boundary case: it lies extremely close to the `D^0 D*+` threshold and is therefore sensitive to long-range pion exchange, heavy-quark symmetry, operator mixing, and unquenched dynamics. These are precisely the sectors where the reduced pure-gauge UIDT scale should not be overextended.

---

## 2. Theoretical Basis

The hybrid UIDT method supplies an unquenched effective gluonic-sector scale

```tex
\Delta^*(N_f)
=
\Delta^*(0)
\sqrt{\frac{33-2N_f}{33}},
\qquad
\Delta^*(0)=1.710~\mathrm{GeV}.
```

For `N_f = 3`, this gives

```tex
\Delta^*(3)
=1.5467531976839273841781459035564202444\ldots~\mathrm{GeV}.
```

This is a [D] unquenched gluonic-sector ansatz inherited from `docs/predictions/unquenched_qcd.md`. Its application to `T_cc+` is further demoted to [E], because the physical state is a coupled-channel hadronic system rather than an isolated gluonic excitation.

---

## 3. Heavy-Light Core-Separation Ansatz

As a deliberately crude diagnostic, define

```tex
M_{raw}(T_{cc}^+)
=
2m_c + 2m_q
+g_{eff}\left[\Delta^*(3)-\delta_{core}\right].
```

Representative inputs:

| Quantity | Value | Evidence | Stratum | Note |
|---|---:|---:|---:|---|
| `Delta*(3)` | `1.546753197683927... GeV` | [D] | III | unquenched UIDT ansatz |
| `m_c` | `1.275 GeV` | [B-context] | I/II | MS-bar charm-mass scale convention |
| `m_q` | `0.005 GeV` | [E] | III | schematic light current-mass proxy, not a constituent mass |
| `delta_core` | `0.200 GeV` | [E] | III | phenomenological diquark-core offset |
| `g_eff` | `1.000` | [E] | III | uncalibrated benchmark |

With these benchmark values,

```tex
M_{raw}
=2(1.275)+2(0.005)+1.000(1.54675319768...-0.200)
=3.90675319768...~\mathrm{GeV}.
```

---

## 4. Threshold Analysis

Using the rounded empirical threshold convention

```tex
E_{thr}=M(D^0)+M(D^{*+})
=1.8648~\mathrm{GeV}+2.0102~\mathrm{GeV}
=3.8750~\mathrm{GeV},
```

the raw UIDT-inspired mapping gives

```tex
M_{raw}-E_{thr}
=0.03175319768...~\mathrm{GeV}
=31.75319768...~\mathrm{MeV}.
```

Thus the raw core-separation ansatz is above threshold. It does not reproduce the observed near-threshold binding.

To match the threshold with all other benchmark inputs fixed, the coupling would need to be

```tex
g_{eff}^{thr}
=0.97642240780379448898...
```

To match a nominal `-273 keV` sub-threshold offset relative to the `D^0D*+` threshold, the coupling would need to be

```tex
g_{eff}^{-273 keV}
=0.97621969805677514610...
```

These fitted numbers are not UIDT predictions. They show the sensitivity of the mapping to long-range and coupled-channel physics.

---

## 5. Chiral and Molecular Boundary

The physical `T_cc+` state is close to the `D^0D*+` threshold. Any realistic description must include:

1. long-range pion exchange;
2. coupled `D D*` channels;
3. heavy-quark spin symmetry;
4. finite-volume effects in lattice comparisons;
5. operator mixing between molecular and compact-diquark interpolators.

The UIDT scale can only enter as an effective gluonic background parameter. It cannot by itself determine the physical binding energy.

---

## 6. Falsification Criteria

This [E] mapping is falsified or abandoned if:

1. unquenched lattice studies show no monotonic relation between heavy-light string tension and the UIDT unquenched beta0-screening factor;
2. the `cc` diquark core cannot be associated with a stable short-distance operator basis;
3. coupled-channel calculations show that the near-threshold binding is fully controlled by pion-exchange dynamics with no residual sensitivity to the gluonic-sector scale;
4. the required fitted `g_eff` varies non-universally across related doubly heavy tetraquark channels.

---

## 7. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Source | Status | Falsification exposure |
|---|---|---:|---:|---:|---|---|---|
| UIDT-MAP-TCC-001 | Raw tetraquark core-separation mapping | `M_raw = 3.90675319768 GeV` | [E] | III | this note; verification script | hypothesis | threshold mismatch |
| UIDT-MAP-TCC-002 | Raw excess over rounded `D^0D*+` threshold | `31.75319768 MeV` | [E] | III | this note; verification script | diagnostic | empirical threshold |
| UIDT-MAP-TCC-003 | Coupling needed to match threshold | `g_eff = 0.9764224078` | [E] | III | this note; verification script | fitted diagnostic | not predictive |
| UIDT-MAP-TCC-004 | Coupling needed for nominal `-273 keV` offset | `g_eff = 0.9762196981` | [E] | III | this note; verification script | fitted diagnostic | not predictive |
| EXT-TCC-001 | `T_cc+` is an observed near-threshold doubly charmed tetraquark candidate | qualitative | [B] | I/II | LHCb arXiv literature | external baseline | none for UIDT by itself |

---

## 8. Verified References

| DOI/arXiv | Status | Used for | Evidence |
|---|---|---|---|
| arXiv:2109.01038 | resolvable | LHCb observation context | [B] |
| arXiv:2109.01056 | resolvable | LHCb threshold/pole-parameter context | [B] |
| arXiv:0805.2999 | resolvable | charm-quark MS-bar mass context | [B-context] |
| arXiv:2108.04785 | resolvable | near-threshold molecular interpretation context | [B-context] |

---

## 9. Reproduction Note

```bash
python verification/scripts/verify_tetraquark_binding_mapping.py
```

The script verifies the arithmetic in this note at local `mp.workdps(80)`. It does not validate the physical tetraquark interpretation.

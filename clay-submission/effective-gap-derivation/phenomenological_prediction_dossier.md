# Phenomenological Prediction Dossier

**UIDT Framework:** v3.9 Canonical  
**Location:** `clay-submission/effective-gap-derivation/`  
**Evidence posture:** [D] predictions built on [A] reduced-model closure and [A-] calibration; [E] interpretive mappings where stated  
**Status:** Draft dossier for reviewer-facing epistemic separation

---

## 1. Methodological Position

The hybrid UIDT method treats the scalar field `S(x)` as an effective parametrization of vacuum information density. The model therefore does not require the claim that `S(x)` is a fundamental elementary field of pure Yang--Mills theory.

This change is not cosmetic. It separates three statements that must never be merged:

| Statement | Evidence | Stratum | Status |
|---|---:|---:|---|
| The reduced algebraic gap equation has a locally contractive fixed point. | [A] | III | internally verified |
| `gamma = 16.339` calibrates the kinetic vacuum sector. | [A-] | III | calibrated |
| The reduced model is equivalent to the full pure Yang--Mills path integral. | [E] | III | open |

The predictive use of the model is allowed only after this separation is explicit. Predictions below are [D] unless explicitly demoted to [E].

---

## 2. Prediction I: Effective Tensor-Glueball Hierarchy

### 2.1 Physical idea

The reduced UIDT scale `Delta* = 1.710 GeV` is used as the scalar anchor for the effective pure-gauge vacuum sector. Higher-spin glueball states are modeled as rotational excitations of an effective flux-tube trajectory.

This is a Regge-style phenomenological ansatz, not a derivation of the complete glueball spectrum.

### 2.2 Formula

```tex
m_J^2 = (\Delta^*)^2 + 2\pi\sigma J.
```

Inputs:

| Quantity | Value | Evidence | Note |
|---|---:|---:|---|
| `Delta*` | `1.710 GeV` | [A] | internal reduced-model closure |
| `sqrt(sigma)` | `0.440 GeV` | [B] | lattice scale convention |
| `J` | `2` | [D] | tensor channel ansatz |

Computation:

```tex
m_{2++}^2 = (1.710)^2 + 2\pi(0.1936)\cdot 2
          = 5.356949351... GeV^2.
```

Prediction:

```tex
m_{2++} = 2.3145084469... GeV  [D]
m_{2++}/m_{0++} = 1.3535137117...  [D]
```

### 2.3 Falsification

The prediction is falsified if future pure-gauge lattice determinations of the tensor/scalar hierarchy, with documented continuum extrapolation and covariance model, exclude

```tex
m_{2++}/m_{0++} = 1.354
```

by more than `2 sigma`.

Agreement may support a [B] lattice-compatible classification. It cannot promote the hybrid method to [A] without the missing projection-equivalence proof.

---

## 3. Prediction II: Confined-Phase Thermal Gap Ansatz

### 3.1 Physical idea

The reduced UIDT scale is coupled to an effective condensate-like vacuum quantity. At finite temperature, the simplest confined-phase ansatz is to let this quantity decrease with `T/T_c`.

This prediction is scoped to the pure SU(3) benchmark. It is not a full-QCD heavy-ion phenomenology claim.

### 3.2 Formula

```tex
C(T) = C(0) [1 - (T/T_c)^4]_+,
Delta_eff(T) = Delta(0) sqrt([1 - (T/T_c)^4]_+).
```

where `[x]_+ = max(0,x)`.

Using `Delta(0)=1.710 GeV` and nominal `T_c=270 MeV`:

| `T` | `Delta_eff(T)` | Evidence |
|---:|---:|---:|
| `100 MeV` | `1.6938 GeV` | [D] |
| `200 MeV` | `1.4296 GeV` | [D] |
| `250 MeV` | `0.8802 GeV` | [D] |
| `270 MeV` | `0.0 GeV` in this ansatz | [D] |

### 3.3 Caveat

The ansatz setting the confined-phase effective scale to zero at `T >= T_c` does not imply that every finite-temperature screening scale is zero. Above the pure-gauge transition, the thermal gauge system still has nonzero screening sectors. The UIDT statement is only that this specific confined-phase effective scale is no longer used beyond its domain.

### 3.4 Falsification

The ansatz is falsified or demoted if finite-temperature pure-gauge lattice correlators in the matched channel cannot be represented by

```tex
Delta_eff(T)/Delta(0) = sqrt(1 - (T/T_c)^4)
```

within documented uncertainties for `T < T_c`.

---

## 4. Prediction III: Effective QGP Shear Viscosity Ansatz

### 4.1 Physical idea

The same confined-phase effective scale can be used to generate a transport ansatz for the shear-viscosity-to-entropy-density ratio `eta/s`. This is not a first-principles transport calculation. It is a phenomenological bridge between the UIDT thermal gap ansatz and real-time transport observables.

The reference value

```tex
(eta/s)_{KSS} = 1/(4 pi)
```

is used as a holographic comparison scale, not as a proven universal theorem for QCD.

### 4.2 Formula

For `T <= T_c`, define

```tex
eta/s(T) = 1/(4 pi) + K [Delta_eff(T)/T]^alpha,
```

with positive phenomenological parameters:

```tex
K > 0,
alpha > 0.
```

The limiting behavior inside this ansatz is

```tex
lim_{T -> T_c^-} eta/s(T) = 1/(4 pi).
```

This is a statement about the ansatz only. It is not a claim that pure SU(3) has a continuous transition, and it is not a full-QCD heavy-ion prediction.

### 4.3 Falsification

The ansatz is falsified or demoted if matched transport reconstructions show that no positive-parameter expression of the above form can describe the relevant channel below `T_c`, or if the transport channel is demonstrably decoupled from the confined-phase screening scale.

A full-QCD heavy-ion comparison requires a separate unquenched UIDT extension.

---

## 5. Prediction IV: Unquenched-QCD Screening Ansatz

### 5.1 Physical idea

Dynamical fermions modify the running of the QCD coupling through the flavor-dependent beta-function coefficient. UIDT uses this standard QCD fact only as a phenomenological screening input for an effective gluonic-sector scale.

This is not a physical mass-gap claim for full QCD. Light pseudoscalar mesons, chiral symmetry breaking, and operator mixing dominate the deep infrared. The ansatz applies only to a specified gluonic operator sector and only after the unquenched lattice extraction protocol is defined.

### 5.2 Formula

For `SU(3)`, the leading beta-function coefficient is

```tex
beta0(N_f) = 11 - (2/3) N_f = (33 - 2 N_f)/3.
```

The UIDT screening ansatz is

```tex
Delta*(N_f) = Delta*(0) sqrt((33 - 2 N_f)/33),
Delta*(0) = 1.710 GeV.
```

Representative values:

| `N_f` | Interpretation | `Delta*(N_f)` | Evidence |
|---:|---|---:|---:|
| 0 | pure Yang--Mills anchor | `1.7100 GeV` | [A] internal anchor |
| 2 | dynamical `u,d` proxy | `1.6027 GeV` | [D] |
| 3 | dynamical `u,d,s` proxy | `1.5469 GeV` | [D] |

### 5.3 Chiral boundary

The pion mass and pion decay constant belong to the light-quark chiral sector. They must not be treated as the screened pure-glue mass scale. In full QCD, scalar and pseudoscalar channels mix gluonic and quark-bilinear operators; therefore a direct one-number identification with `Delta*(N_f)` is not justified without a matched operator analysis.

### 5.4 Falsification

This ansatz is falsified or demoted if unquenched lattice calculations show that the effective gluonic-sector scale does not decrease with active light flavors, that the square-root `beta0` response fails against a better-supported scaling law, or that operator mixing prevents a stable gluonic-sector scale from being defined.

---

## 6. Mapping V: Tetraquark `T_cc+` Binding-Energy Diagnostic

### 6.1 Physical idea

The exotic open-charm tetraquark `T_cc+` is a boundary test for overextending the unquenched UIDT scale. It lies close to the `D^0D*+` threshold, where long-range pion exchange, coupled-channel effects, and heavy-quark symmetry are essential.

This item is therefore [E], not [D]. It is an interpretive mapping designed to expose where the gluonic-sector ansatz stops being sufficient.

### 6.2 Formula

A crude heavy-light core-separation diagnostic is

```tex
M_raw(T_cc+) = 2 m_c + 2 m_q + g_eff [Delta*(3) - delta_core].
```

Using the benchmark values

```tex
Delta*(3) = 1.546753197683927... GeV,
m_c = 1.275 GeV,
m_q = 0.005 GeV,
delta_core = 0.200 GeV,
g_eff = 1.000,
```

the raw mapping gives

```tex
M_raw = 3.90675319768... GeV  [E].
```

Against the rounded threshold

```tex
M(D^0) + M(D*+) = 1.8648 GeV + 2.0102 GeV = 3.8750 GeV,
```

the raw excess is

```tex
M_raw - E_thr = 31.75319768... MeV  [E].
```

Thus the raw UIDT-inspired mapping is above threshold. It does not reproduce the observed near-threshold binding.

### 6.3 Diagnostic fitted couplings

Holding all other benchmark inputs fixed:

```tex
g_eff(threshold) = 0.9764224078037944...,
g_eff(-273 keV) = 0.9762196980567751....
```

These are fitted diagnostics, not predictions.

### 6.4 Falsification

This mapping is falsified or abandoned if the heavy-light string tension shows no monotonic relation to the unquenched beta0-screening factor, if the `cc` diquark cannot be isolated in a stable operator basis, or if coupled-channel calculations show that the near-threshold binding is fully controlled by pion-exchange dynamics with no residual gluonic-scale sensitivity.

---

## 7. External Baselines

| DOI/arXiv | Status | Used for | Evidence |
|---|---|---|---|
| arXiv:hep-lat/9901004 | resolvable | SU(3) glueball spectrum baseline | [B] |
| DOI:10.1103/PhysRevD.60.034509 | resolvable | journal version of Morningstar--Peardon | [B] |
| arXiv:2106.00364 | resolvable | SU(N) glueball/string-tension baseline | [B] |
| DOI:10.1007/JHEP12(2021)082 | resolvable | journal version of Athenodorou--Teper | [B] |
| arXiv:hep-lat/9602007 | resolvable | pure SU(3) thermodynamic scale | [B] |
| DOI:10.1016/0550-3213(96)00170-8 | resolvable | journal version of Boyd et al. | [B] |
| arXiv:hep-th/0405231 | resolvable | KSS reference scale | [B-context] |
| arXiv:0704.1801 | resolvable | SU(3) gluodynamics viscosity baseline | [B] |
| arXiv:1804.06469 | resolvable | Bayesian full-QCD heavy-ion transport context | [B-context] |
| arXiv:2106.05019 | resolvable | later Bayesian QGP transport context | [B-context] |
| arXiv:1701.01404 | resolvable | high-order QCD beta-function context | [B] |
| arXiv:1208.1858 | resolvable | `2+1` unquenched glueball spectrum context | [B] |
| arXiv:1702.08174 | resolvable | `N_f=2` unquenched glueball spectrum and mixing context | [B] |
| arXiv:1406.4987 | resolvable | chiral symmetry breaking and condensate context | [B] |
| arXiv:2109.01038 | resolvable | LHCb `T_cc+` observation context | [B] |
| arXiv:2109.01056 | resolvable | LHCb `T_cc+` threshold/pole-parameter context | [B] |
| arXiv:0805.2999 | resolvable | charm-quark MS-bar mass context | [B-context] |
| arXiv:2108.04785 | resolvable | near-threshold molecular interpretation context | [B-context] |

---

## 8. Reproduction Note

```bash
python verification/scripts/verify_effective_gap_predictions.py
python verification/scripts/verify_unquenched_qcd_ansatz.py
python verification/scripts/verify_tetraquark_binding_mapping.py
```

The first command verifies the reduced-model RG closure, tensor prediction, and thermal input. The second command verifies the unquenched-QCD screening ansatz numerics. The third command verifies only the tetraquark mapping arithmetic. None of these commands proves the physical validity of the phenomenological mappings.

---

## 9. Non-Inflation Rule

These predictions can strengthen UIDT only as falsifiable phenomenology. They do not convert the hybrid effective method into a Clay-level proof. The missing proof remains the equivalence between the reduced effective projection and the full pure Yang--Mills path integral.

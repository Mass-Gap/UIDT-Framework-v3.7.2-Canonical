# Phenomenological Prediction Dossier

**UIDT Framework:** v3.9 Canonical  
**Location:** `clay-submission/effective-gap-derivation/`  
**Evidence posture:** [D] predictions built on [A] reduced-model closure and [A-] calibration  
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

The predictive use of the model is allowed only after this separation is explicit. The predictions below are therefore [D], not [A].

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

## 5. External Baselines

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

---

## 6. Reproduction Note

```bash
python verification/scripts/verify_effective_gap_predictions.py
```

This verifies the reduced-model RG closure, tensor prediction, and thermal input. No first-principles transport solver is introduced by the QGP viscosity note.

---

## 7. Non-Inflation Rule

These predictions can strengthen UIDT only as falsifiable phenomenology. They do not convert the hybrid effective method into a Clay-level proof. The missing proof remains the equivalence between the reduced effective projection and the full pure Yang--Mills path integral.

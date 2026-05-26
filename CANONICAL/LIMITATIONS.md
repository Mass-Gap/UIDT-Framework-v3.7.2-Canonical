# UIDT Known Limitations v3.7.2 + WP1 Addendum

> **PURPOSE:** Transparent documentation of unresolved issues  
> **PRINCIPLE:** Acknowledge what we don't know

---

## Active Limitations (Unresolved)

### L1: Geometric Scale Factor (Ill-Defined)
**Status:** 🔬 HIGHEST PRIORITY — PROBLEM STATEMENT REQUIRES CLARIFICATION

**Description:**  
Previous versions stated "a factor of ~10¹⁰" without specifying reference scales.
mpmath 80-dps analysis (TKT-20260416-L1L4L5-analysis.md) reveals:

  λ_UIDT / r_conf = 0.660 nm / 0.197 fm = 3.35 × 10⁶ ≈ 10^6.5 (NOT 10¹⁰)

The actual ratio depends on which UV/IR scales are compared. No energy ratio
in the Standard Model yields exactly 10¹⁰. Closest approach: λ_UIDT/r_conf ≈ α⁻³ × 1.302.

**Impact:**  
- λ_UIDT calibrated [C] instead of derived [A]
- The problem is real but was previously ill-defined

**Condition for Resolution:**  
1. Precisely define which UV and IR scales are compared
2. Derive the geometric factor from first principles (topology, holography, or α⁻³ connection)

---

### L2: Electron Mass Discrepancy
**Status:** ⚠️ PARTIAL

**Description:**  
Electron mass formula shows 23% residual (was 3.2% in earlier versions).

**Impact:**  
- m_e prediction remains approximate
- Electroweak sector not fully integrated

**Condition for Resolution:**  
Improved electroweak coupling in UIDT framework

**Note:** v3.6.1 patch addressed some issues but not fully resolved.

---

### L3: Vacuum Energy Residual
**Status:** ✅ ACCEPTED

**Description:**  
Vacuum energy prediction ρ_vac differs from Λ_QCD calibration by factor ~2.3.

**Impact:**  
- Order-of-magnitude correct (vs. 10¹²⁰ problem)
- Factor 2.3 within theoretical uncertainty

**Resolution:**  
Accepted as within framework tolerance. 99-step RG cascade + π⁻² normalization addresses 10¹²⁰ catastrophe.

---

### L4: γ Not Derived from RG
**Status:** 🔬 ACTIVE RESEARCH

**Description:**  
γ = 16.339 is phenomenologically determined from kinetic VEV, NOT derived from RG flow equations.

**Impact:**  
- γ is Category [A-] not [A]
- Claims of "first-principles" derivation are INCORRECT
- Perturbative RG gives γ* ≈ 55.8 (factor 3.4 discrepancy)

**Condition for Resolution:**  
- Show γ = 49/3 = (2Nc+1)²/Nc from QCD
- OR derive from non-perturbative FRG
- OR accept as empirical constant

**Note:** In RESEARCH-MODE, exploring γ derivation is permitted with [E] tag.

---

### L5: N=99 RG Steps Unjustified
**Status:** 🔬 ACTIVE RESEARCH

**Description:**  
The 99-step RG cascade is empirically chosen; no theoretical derivation exists.

**Impact:**  
- Vacuum energy suppression mechanism phenomenological
- Raises question: why exactly 99?

**Condition for Resolution:**  
Physical/mathematical derivation of N=99 from first principles

**Hypotheses:**
- Related to number of SM degrees of freedom?
- Holographic dimension counting?
- Accidental numerical coincidence?

---

### L6-FRG: FRG Derivation of γ — Minimal Truncation (S F² Sector)
**Status:** 🔬 ACTIVE RESEARCH — linked to GAP-FRG-001

**Description:**  
The FRG analysis of Claim UIDT-C-070 (eta_* ≈ 0.072, Evidence D) is based on a minimal
truncation with the following deliberate methodological compromises:

- **η_A = 0:** Gluon anomalous dimension set to zero (background-field approximation).
  Gluon fluctuations in the anomalous dimension scheme are not fully captured.
- **Massless scalar:** The scalar S is treated as massless (w_S → 0 limit).
- **4×4 truncation only:** The coupling space is {g², λ_S, κ², κ²} without higher operators.
- **LPA (Local Potential Approximation):** No momentum-dependent vertex projection (∂_p²).
  The beta-functions are evaluated at p² = 0 only.
- **Litim regulator in conformal window:** The threshold functions are evaluated in the
  w → 0 limit, suppressing IR mass effects.

**Impact on current results:**  
- The anomalous dimension η_* ≈ 0.072 is a truncation-dependent result (Evidence D).
- Complex eigenvalues (±0.654i) of the stability matrix indicate a spiralling RG flow
  in the IR — classified as a truncation artefact from missing higher operators (S²F²).
- The gap Δη ≈ 0.009 between η_* and the phenomenological threshold ≈ 0.063 is
  consistent with the expected effect of missing gluon fluctuations.

**What this limitation does NOT affect:**  
- The canonical value γ = 16.339 (Evidence A-) is independent of this truncation.
  It is a kinematic calibration, not derived from the FRG run.
- The Yang-Mills spectral gap Δ* = 1.710 ± 0.015 GeV (Evidence A) is not affected.

**Condition for Resolution:**  
See clay-submission/GAP_ANALYSIS_CLAY.md → GAP-FRG-001 for the full solution path.
Resolution requires a momentum-dependent vertex projection (∂_p²) and a
self-consistent Dyson resummation in the full (S, A) propagator matrix.

---

### L8: EFT Validity Domain and UV Completion
**Status:** 🔬 OPEN — Defines proof scope for WP-1

**Description:**  
UIDT is formulated as an effective field theory (EFT) below a UV cutoff Λ_UIDT.
The non-minimal coupling (κ̄/Λ_UIDT) S F^a_μν F^aμν is a dimension-5 operator and
is therefore non-renormalisable by strict power counting. Its validity is restricted
to the EFT domain p ≪ Λ_UIDT. A full non-perturbative UV completion remains an
open research question.

**Scope defined by PI Decision D-18 (2026-05-26):**  
All WP-1 derivations (Lemma C, Gap-Inheritance, Wilson projection) are explicitly
scoped to the IR regime p ≪ Λ_UIDT ≈ 1.0 GeV. This is the EFT-Path (Option A).
The decision is binding: no WP-1 claim may invoke UV physics beyond this cutoff
without a new formal PI decision.

**What L8 protects:**  
- Lemma C (Gap-Inheritance) remains valid in the IR regardless of UV completion status.
- The Banach fixed-point result (Theorem S1) is IR-regime constructive evidence [A-];
  it does not require UV completion for its local validity.
- Claims C-101 and C-102 are scoped to p ≪ Λ_UIDT throughout.

**What L8 does NOT affect:**  
- The spectral gap Δ* = 1.710 ± 0.015 GeV [A] and VEV v = 47.7 MeV [A].
- The RG constraint |5κ² − 3λ_S| < 10⁻¹⁴ [A].

**Condition for Resolution:**  
Asymptotic safety at the non-perturbative level (non-trivial UV fixed point of the
full RG flow), or identification of a renormalisable UV embedding. Until then:
Closure language is FORBIDDEN for claims that invoke physics above Λ_UIDT.

---

### L9: OS Construction and Global Existence
**Status:** 🔬 OPEN — Explicitly out of scope for current WP-1 programme

**Added:** 2026-05-26 | **Source:** WP1-emergence-chain.md Step 5

**Description:**  
The Osterwalder–Schrader (OS) construction — reflection positivity, clustering,
spectral condition, and controlled infinite-volume limit on all of ℝ⁴ — is not
addressed by the local Banach fixed-point approach of WP-1 Steps 1–3.

The Clay Millennium Problem criterion (Jaffe–Witten) requires:
1. A quantum Yang–Mills theory on ℝ⁴ as a rigorously defined measure on the
   space of gauge field configurations (OS axioms).
2. A proof that the Hamiltonian's spectral gap survives the infinite-volume limit.

UIDT currently provides:
- Local constructive evidence for a spectral gap Δ* within the UIDT axiom
  system [A-] — not a global proof.
- Lattice-compatible numerical verification at z = 0.37σ [B].
- A derivation programme for effective SU(3) structure (WP-1 Steps 1–4).

UIDT does NOT currently provide:
- A globally defined OS measure on all of ℝ⁴.
- A proof of global uniqueness of the vacuum on the full configuration space.
- A Clay-compatible existence theorem.

**Impact on WP-1:**  
- Δ* is locally constructed, not globally proven.
- Lemma C (Gap-Inheritance) is valid in the EFT domain (L8 scope) but does not
  constitute a Clay-level proof.
- C-101, C-102 cannot be promoted beyond [D] without OS construction.

**Complementarity framing:**  
Clay asks: *Given SU(3) Yang–Mills, does it have a mass gap?*  
UIDT asks: *Which vacuum structure forces the emergence of a theory with a mass gap?*  
These are different questions. A Clay solution would establish the gap within SU(3).
UIDT attempts to explain WHY SU(3) has this gap from a deeper structure.

**Condition for Resolution:**  
Independent programme; requires constructive QFT methods
(Glimm–Jaffe, *Constructive Quantum Field Theory*). Minimum requirements:
- Reflection positivity proof for UIDT Banach fixed point
- Controlled infinite-volume limit with maintained gap
- Compliance with all OS axioms

**Closure language:** FORBIDDEN for this limitation. Terms "proves", "solves",
"resolves", "definitive" are blocked for any claim touching L9.

---

## PI Decision Log (WP-1 Relevant)

### D-18: SCALAR-TENSION-001 — Coupling Term Dimension Choice
**Date:** 2026-05-26  
**Status:** ✅ DECIDED — Option A (EFT-Path / Hard-Cutoff)

**Decision:**  
The non-minimal coupling term in the UIDT Lagrangian is fixed as the dimension-5
EFT operator:

```
L_int = (κ̄ / Λ_UIDT) · S · F^a_μν F^aμν
```

This is Option A (EFT-path, dim-5). Option B (dim-6, renormalisable, κ S² Tr(FF))
and Option C (topological path) are REJECTED for the following reasons:

**Rationale for Option A:**
- Consistent with Axiom 2 of the Ontology document (DOI: 10.5281/zenodo.20319634),
  which explicitly states the coupling has mass dimension 5 and is EFT-only.
- Consistent with the v4.1 audit form of the Lagrangian.
- L8 (EFT validity domain) provides formal protection: proof validity is IR-scoped,
  no UV promise is made.
- Does NOT introduce new epistemic debt beyond existing L8.

**Rationale against Option B:**
- NLO-RG corrections (C-096) and parameterless γ-derivation (C-016, L4) are [E].
- Building Lemma C on a dim-6 operator would propagate [E] evidence into the
  Gap-Inheritance argument, demoting C-102 to [E].

**Rationale against Option C (topological path):**
- L5 (topological susceptibility tension, 4.25σ vs. Dürr et al. 2025) is unresolved.
- Any topological proof step would immediately trigger the L5 kill-switch.

**Consequences for WP-1:**
- O-SC (SCALAR-TENSION-001) is RESOLVED → Status: closed
- Step 4 (Wilson Projection) unblocked: proceed with dim-5 EFT operator
- Lemma C validity domain: p ≪ Λ_UIDT ≈ 1.0 GeV
- All downstream claims (C-101, C-102) carry the L8 EFT scope restriction

**Authorisation:** P. Rietz (PI) | Branch: feat/WP1-emergence-chain

---

## Resolved Limitations (Historical)

### L6: Spectral Gap vs. Particle Mass [RESOLVED — superseded by L6-FRG above]
**Status:** ✅ CLARIFIED (2025-12-25)

**Previous Issue:**  
Δ = 1.710 GeV was sometimes conflated with glueball mass.

**Resolution (2025-12-25):**  
Δ is the SPECTRAL GAP of Yang-Mills Hamiltonian, NOT a particle mass.
Glueball identification explicitly WITHDRAWN [E].

*Note: The label L6 has been reused for L6-FRG (active, 2026-04-06).
This historical entry is preserved for audit continuity.*

---

### L7: VEV Value [RESOLVED]
**Status:** ✅ CORRECTED

**Previous Issue:**  
v = 0.854 MeV in Framework v3.2

**Resolution (v3.6.1):**  
Corrected to v = 47.7 MeV. Old value was erroneous.

---

## Limitation Impact Matrix

| ID      | Limitation                          | Impact on Claims              | Priority    |
|---------|--------------------------------------|-------------------------------|-------------|
| L1      | Geometric scale (~10^6.5, ill-defined)| λ_UIDT [C→D if unresolved]    | 🔴 High     |
| L2      | Electron mass                        | m_e formula approximate       | 🟡 Medium   |
| L3      | Vacuum energy                        | ρ_vac factor 2.3              | 🟢 Accepted |
| L4      | γ not from RG                        | γ remains [A-] not [A]        | 🔴 High     |
| L5      | N=99 unjustified                     | RG cascade phenomenological   | 🟡 Medium   |
| L6-FRG  | FRG minimal truncation (C-070)       | η_* Evidence D, not upgradable| 🔴 High     |
| L8      | EFT validity / UV completion         | WP-1 proof scoped to IR only  | 🟡 Medium   |
| L9      | OS construction / global existence   | No Clay-level proof           | 🔴 High     |

---

## Falsification Triggers

If any of these occur, UIDT requires major revision:

1. **Lattice QCD:** Δ ≠ 1.710 GeV at >3σ
2. **Casimir:** |ΔF/F| < 0.1% at d ≈ 0.66 nm (no anomaly)
3. **DESI:** w = -1.00 ± 0.01 exactly (pure ΛCDM)
4. **LHC:** Scalar excluded in 1.5-1.9 GeV window

See `LEDGER/FALSIFICATION.md` for details.

---

**CITATION:** Rietz, P. (2025/2026). UIDT v3.9. DOI: 10.5281/zenodo.17835200

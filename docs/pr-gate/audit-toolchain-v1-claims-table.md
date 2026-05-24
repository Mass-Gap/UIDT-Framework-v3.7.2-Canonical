# PR Gate — UIDT Audit Toolchain v1
## Branch: `feature/audit-toolchain-v1`  |  PR #502
**Last updated:** 2026-05-24 (Patch v4 — [D]→[B] coefficient upgrade)

---

## Claims Table

| Claim ID | Value | Evidence Tag | Stratum | Status | Falsification Exposure |
|---|---|---|---|---|---|
| **C-RG-01** | $\|5\kappa^2 - 3\lambda_S\| < 10^{-14}$ (exact algebraic) | **[A]** | III | ✅ VERIFIED | Violated if computer algebra shows constraint not satisfied |
| **C-RG-02** | $\beta_\kappa^{(1)} = \kappa/(16\pi^2)[4(\lambda_S+\kappa^2)-g_3^2 N_c]$ | **[A]** | III | ✅ VERIFIED | Any symbolic CAS contradiction |
| **C-RG-03** | $\beta_\kappa^{(2)}$ coeff A=+12, B=−48, C=+12, D=−12 (M-V 1985) | **[B]** | II/III | ✅ UPGRADED [D→B] | Independent M-V coefficient lookup; Feynman diagram cross-check |
| **C-RG-04** | $\beta_{\lambda_S}^{(2)}$ coeff E=−144, F=+96, G=−24, H=−24 (M-V 1985) | **[B]** | II/III | ✅ UPGRADED [D→B] | Same; phi^4 limit regression [A]-verified |
| **C-RG-05** | phi^4 regression: $g_3,\kappa\to 0$ recovers $-144\lambda_S^3/(16\pi^2)^2$ | **[A]** | II | ✅ VERIFIED | Residual > $10^{-60}$ at dps=80 |
| **C-STAB-01** | Stability eigenvalues at canonical point (Jacobian numerical) | **[B]** | III | ✅ IMPLEMENTED | Eigenvalue sign reversal under lattice $g_3$ |
| **C-VAC-01** | $\rho_{\rm vac} = \rho_{\rm QFT}\times\pi^{-2}\times\prod_{n=1}^{99}f_n(g)$ | **[C]** | III | ❌ **[AUDIT_FAIL]** | $f_n$ not in repository; L1 open |
| **C-VAC-02** | Parametric $f_n$: Exponential/Power-law/Rational families scan | **[D]** | III | ⚠️ PARTIAL | Implemented in `vacuum_suppression.py --profile parametric` |
| **C-VAC-03** | $\Delta_{\rm FT}$ Barbieri-Giudice for $f_n$ families | **[D]** | III | ⚠️ PARTIAL | Blocked by L-fn |
| **C-UV-01** | $\kappa=0.5$ protected by $\mathbb{Z}_N$ discrete shift symmetry | **[D]** | III | ⚠️ DRAFT | Symmetry argument in `docs/uv_mechanism_note.md` |
| **C-UV-02** | Large-N collective: $N_f=10$, $y\approx 0.72$, $M_F=0.3\Lambda_{\rm UV}$ gives $\kappa\approx 0.5$ | **[D]** | III | ⚠️ DRAFT | Fails if $\kappa_{\rm UV}>1$ in explicit UV completion |
| **C-UV-03** | Sequestered RS1: $\kappa_{\rm 5D}\approx 2$, $kL\approx 11.5$ | **[D]** | III | ⚠️ DRAFT | Fails if RS1 KK-spectrum excludes $\Delta\approx 1.71$ GeV |
| **C-TOOL-01** | All scripts pass SHA256 verification (Dockerfile pinned) | **[A]** | I | ✅ VERIFIED | Hash mismatch |

---

## Evidence Upgrade Log

| Date | Claim | Old Tag | New Tag | Justification |
|---|---|---|---|---|
| 2026-05-24 | C-RG-03 | [D] | **[B]** | M-V (1985) Nucl.Phys.B249 Table 6; topology A–D enumerated |
| 2026-05-24 | C-RG-04 | [D] | **[B]** | M-V (1985) Nucl.Phys.B249 Table 7; phi^4 limit [A]-verified |
| 2026-05-24 | C-STAB-01 | [D] | **[B]** | Jacobian numerical, M-V framework standard QFT |

> **Guardian Consensus Note:** Evidence upgrades [D]→[B] require 3-agent veto chain (SKILL-2: uidt-guardian-consensus). Pending: Reviewer → Regressed → Auditor sign-off on C-RG-03, C-RG-04, C-STAB-01.

---

## Hard Blockers (must resolve before merge)

| ID | Blocker | Owner | Deadline |
|---|---|---|---|
| **L-fn** | `f_n(g)` definitions not in LEDGER/CLAIMS_ADDENDUM_C054_C056 | P. Rietz | TBD |
| **L-guardian** | Guardian 3-agent sign-off on [B] upgrades | Reviewer+Regressed+Auditor | Before merge |
| **L-g3** | $g_3^2$ lattice value at $m_S=1.705$ GeV to replace perturbative estimate | Lattice reviewer | Before merge |

---

## One-Command Reproduction

```bash
docker build -t uidt-audit . && docker run --rm -v $(pwd)/results:/app/results uidt-audit
```

## DOI / arXiv Resolvability

| DOI/Ref | Status | Used for | Evidence Tag |
|---|---|---|---|
| 10.5281/zenodo.17835200 | ✅ Resolvable | Framework canonical values | [A] |
| M-V Nucl.Phys.B249(1985)70 | ✅ Published journal | 2-loop scalar quartic coefficients | [B] |
| M-V Nucl.Phys.B222(1983)83 | ✅ Published journal | 2-loop wave-function renorm | [B] |
| M-V Nucl.Phys.B236(1984)221 | ✅ Published journal | 2-loop Yukawa | [B] |

---

## Suggested Reviewers

| Role | Scope |
|---|---|
| **RG/β-expert** | M-V coefficient verification; stability analysis |
| **Lattice QCD contact** | $\alpha_s(m_S)$, $\Delta=1.710$ GeV compatibility |
| **EFT/UV expert** | `uv_mechanism_note.md` matching formulas |

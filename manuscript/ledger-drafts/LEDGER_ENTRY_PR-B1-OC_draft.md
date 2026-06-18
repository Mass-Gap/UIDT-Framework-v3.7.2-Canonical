# LEDGER ENTRY DRAFT — PR-B1 Outcome O-C (Honest Null)

| Field | Value |
|---|---|
| Entry ID | `LEDGER-PR-B1-OC-001` (DRAFT for PI review and commit) |
| Target path | `LEDGER/CLAIMS.json` (protected — PI commits, not Claude) |
| Author of draft | Claude/Opus, advisory capacity. **This is a draft only.** The PI enters it into the protected ledger and signs. |
| Source of fact | `PREREG-PR-B1-PRE-001` (PI-signed 2026-06-17, OUTCOME RECORDED: PRE-O1) |
| Corroboration | `RESEARCH-YMCS-METASTAB-001` (Azuma et al. JHEP 05 (2004) 005 + corroborating, primary PDFs read) |
| Evidence class | **[D]** — research-programme outcome; authorizes no upgrade. Cosmology cap N/A. |

---

## 1. What is being recorded

PR-B1 (does YMCS matrix condensation thermodynamically select the Wedderburn partition `(2,3)`?) is recorded as outcome **O-C: honest null**. The standard YMCS/Myers model does **not** isolate `(2,3)` as a stable vacuum. A planted `(2,3)` decays out of the `(2,3)` class by MC step ~10 at every tested coupling, confirming the literature null (single fuzzy sphere is the true vacuum) with our own blind, validated PR-B0.2 detector.

This **reinforces** Appendix B Rem. B-moduli-restated and does **not** support Conjecture C-B1 (stays [E]). ONT-08 stays [D]. No constant, no evidence class, and no claim is upgraded.

## 2. Exact facts (from the signed pre-protocol, nothing added)

- **Model:** M0 (YMCS/Myers, undeformed): `S = N tr(−¼[X_a,X_b]² + (2/3)iα ε_abc X_a X_b X_c)`.
- **Coupling window (blind, literature-anchored):** α̃ ∈ {0.40, 0.55, 0.625, 0.75, 0.90}, straddling α̃_c = 0.625 ± 0.125 (arXiv:2007.04488).
- **N ladder:** {16, 24, 32}.
- **Result:** planted `(2,3)` decayed completely out of the `(2,3)` class by step ~10 of HMC thermalization in **all** configurations.
- **Outcome:** PRE-O1 (literature null confirmed). Detector = PR-B0.2 grid detector, τ=0.14; δ measured, finite-K factor A (1/0.987) frozen; blindness PI-confirmed.

## 3. What this does NOT claim (guard against over-reading)

- It does **not** claim the Standard Model gauge group is excluded by physics — only that *this single-trace bosonic model* does not select `(2,3)`.
- It does **not** claim `(2,3)` is impossible in any model — the question of whether a *deformation* stabilizes it is PR-B2, open.
- It is a **measured null for M0**, not a statement about UIDT's correctness. The attractor hypothesis ends here only at the partition-selection level for the undeformed model.

## 4. Consequential action recorded alongside

- **Full PR-B1-002 base-model run: CANCELLED** as not required — the question is answered by PRE-O1 plus verified literature. (Optional corroboration only, at PI discretion.)
- **PR-B2 opened** as an honest [D]/[E] programme charter: "does any deformation force a stable asymmetric `(2,3)` vacuum?" — currently UNSOLVED per all verified literature, including arXiv:2601.14141 (which shows only a single-matrix H→−H 2-cut, not a Wedderburn block split — see PR-B2 charter).

## 5. Proposed `CLAIMS.json` block (for PI to paste and commit)

```json
{
  "id": "PR-B1",
  "title": "YMCS matrix condensation vs. Wedderburn (2,3) selection",
  "outcome": "O-C",
  "outcome_label": "honest null — YMCS/Myers (M0) does not select (2,3) as a stable vacuum",
  "evidence_class": "D",
  "strata": "III",
  "status": "RECORDED",
  "method": "blinded HMC metastability pre-protocol (PREREG-PR-B1-PRE-001), PR-B0.2 grid detector, tau=0.14, delta measured (finite-K factor A)",
  "result_summary": "planted (2,3) decays out of (2,3) class by MC step ~10 at all alpha_tilde in {0.40,0.55,0.625,0.75,0.90}, N in {16,24,32}",
  "preregistered_null": "single fuzzy sphere is true vacuum (Azuma et al., JHEP 05 (2004) 005)",
  "blindness": "PI-confirmed; alpha_tilde/N/tau/delta frozen pre-results",
  "corroboration": ["10.1088/1126-6708/2004/05/005", "RESEARCH-YMCS-METASTAB-001"],
  "reinforces": "Appendix B Rem. B-moduli-restated",
  "does_not_upgrade": ["C-B1 (stays E)", "ONT-08 (stays D)"],
  "full_run_PR-B1-002": "CANCELLED — not required (answered by PRE-O1 + literature)",
  "successor": "PR-B2 (open [D]/[E] charter: deformation-stabilized (2,3)? UNSOLVED)",
  "signed_source": "PREREG-PR-B1-PRE-001 (PI-signed 2026-06-17)",
  "pi_signoff": "PENDING — PI enters and signs",
  "date_recorded": "2026-06-17"
}
```

## 6. Suggested commit (PI executes; GPG-sign if available)

```
git add LEDGER/CLAIMS.json
git commit -S -m "PR-B1 = O-C honest null: YMCS/Myers does not select (2,3); PR-B1-002 base run cancelled; PR-B2 opened"
```

(If no GPG: plain commit under your authenticated GitHub account. The signed pre-protocol is the human-readable provenance; the commit is the tamper-evident anchor.)

## 7. Pre-commit checklist (advisory)

- [ ] `outcome` = O-C, `evidence_class` = D — matches the signed pre-protocol.
- [ ] No constant/claim upgraded; C-B1 stays [E], ONT-08 stays [D].
- [ ] Result summary states only what the pre-protocol observed (decay by step ~10), nothing added.
- [ ] Full PR-B1-002 base run marked CANCELLED, not silently dropped.
- [ ] PR-B2 referenced as open/unsolved, Dirac not pre-declared as solution.
- [ ] No forbidden verdict words; no process/tooling language in the ledger value.

---

*Draft by Claude/Opus, advisory capacity. Records the PI-signed PRE-O1 outcome faithfully and adds nothing beyond it. Entry into the protected `LEDGER/` path and the signature are the PI's action; this draft authorizes nothing.*

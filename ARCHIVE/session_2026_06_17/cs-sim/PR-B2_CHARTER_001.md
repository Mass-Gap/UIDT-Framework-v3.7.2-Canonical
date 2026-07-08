# PR-B2 — Programme Charter: Does Any Deformation Force a Stable Asymmetric (2,3) Wedderburn Vacuum?

| Field | Value |
|---|---|
| Charter ID | `PR-B2-CHARTER-001` (DRAFT for PI review) |
| Type | Honest research-programme charter. **Not** an implementation mandate. No mechanism is pre-declared as the solution. |
| Predecessor | PR-B1 = O-C (honest null): YMCS/Myers (M0) does not select `(2,3)` (`LEDGER-PR-B1-OC-001`). |
| Author | Claude/Opus, advisory capacity. Authorizes nothing; the PI decides scope and sign-off. |
| Evidence ceiling | Every candidate mechanism enters at its **verified** class: [D]/[E] for anything claimed to *produce* asymmetric `(2,3)`; [B] only for the established *negative* results. No [A]. Cosmology N/A. |
| Style precedent | Appendix B Connes-vacuum charter (PI-endorsed): speculative mechanisms held at [D]/[E]; fabricated proofs refused. |

---

## 1. The question, stated honestly

PR-B1 established that the undeformed single-trace bosonic YMCS/Myers model does **not** select the asymmetric Wedderburn partition `(2,3)` (↔ `SU(2)⊕SU(3)`); a planted `(2,3)` decays to the single-sphere vacuum. PR-B2 asks the genuinely open successor question:

> **Does there exist any deformation of the matrix model that makes an asymmetric `(2,3)` Wedderburn partition the stable global minimum (true vacuum) — spontaneously, not by hand-inserted symmetry breaking?**

**Honest status up front:** per all primary literature verified this session, **no such mechanism is currently known.** PR-B2 is therefore an open [D]/[E] search, not the implementation of a known solution. This charter exists precisely so the search is not mis-started on an over-claimed premise.

## 2. Why this charter is needed (the over-claim it guards against)

During PR-B1 a document (`Symmetriebrechung.txt`) claimed the Dirac operator / spectral action is "the only known and verified mechanism" forcing a stable `(2,3)` Wedderburn vacuum, citing arXiv:2601.14141. **Full-text verification this session refuted that reading:** arXiv:2601.14141 (D'Arcangelo & Gnutzmann 2026) treats the **single-matrix** (1,0)/(0,1) Dirac ensembles and finds a real `H→−H` symmetry-breaking **2-cut** transition — *two eigenvalue intervals of one matrix*, not two algebra blocks. The terms "Wedderburn", "`SU(2)⊕SU(3)`", and "`M₂(ℂ)⊕M₃(ℂ)`" do not appear. Reading a 2-cut spectrum as a block decomposition is a **category error**. PR-B2 records the Dirac route as an *interesting open thread*, not a solution.

## 3. Verified evidence table for candidate mechanisms (primary sources)

Each mechanism is logged at the class actually supported by sources read or verified this session.

| Mechanism | Source (verification status) | What is established | Class | Forbidden inference |
|---|---|---|---|---|
| **Massive Myers** `½m²Tr A²` | Azuma-Bal-Nishimura PRD72(2005)066005 (read via uploads) | Stable multi-block phase exists, but blocks are **equal size** (symmetric `U(k)`); window `8m²<α²<9m²` | **[B]** for equal-block `U(k)`; asymmetric `(2,3)` not produced | Does not yield asymmetric `(2,3)` |
| **Asymmetric Myers / anisotropic flux** | Steinacker-Zahn arXiv:1401.2020 (cited, not independently fetched) | Can embed an SM-like brane config, but needs **hand-inserted** `SO`-breaking mass terms ("squashed branes") | **[D]** — explicit breaking by hand | Brute-force embedding, not spontaneous emergence |
| **Fermions / SUSY** | Anagnostopoulos-Azuma-Nagao-Nishimura hep-th/0506062 (cited) | SUSY stabilizes the **single** sphere absolutely, **destabilizes** `k>1`; gauge group → `U(1)` | **[B]** for the no-go (`SUSY→U(1)`) | Fermions make it **worse**, not better |
| **Dirac / spectral action** | arXiv:2601.14141 **full text read**; Khalkhali-Pagliaroli; Barrett-Glaser | Real `H→−H` 2-cut in the **single-matrix** Dirac ensemble; no multi-matrix gauge structure, no block split | **[D]** — single-matrix spectral SB; bridge to a gauge-group Wedderburn split is **unbuilt** | 2-cut spectrum ≠ block decomposition (category error) |
| **Multi-trace deformation** `−β(Tr D²)²+γ Tr D⁴` | Pérez-Sánchez arXiv:2007.10914 (cited); general spectral action | Spectral action **does** generate multi-trace terms naturally; **no proof** they select asymmetric `(2,3)` as global min | **[D]/[E]** — plausible direction, no existence proof | Generates multi-trace dynamics; does **not** prove `(2,3)` selection |

**Bottom line (recorded):** no mechanism is verified to force a stable asymmetric `(2,3)` Wedderburn vacuum as global minimum. The established results are the *negative* ones (equal-block `U(k)` [B]; `SUSY→U(1)` no-go [B]). Everything claimed to *produce* `(2,3)` sits at [D]/[E].

## 4. What PR-B2 may legitimately pursue (open threads, not mandates)

Listed as research directions, each with its own falsification/downgrade condition. None is the designated answer.

1. **Multi-trace bridge thread [D]/[E].** Investigate whether spectral-action multi-trace terms, in a genuine **multi-matrix** setting (not the single-matrix (1,0)/(0,1) ensemble), can select an asymmetric block partition. *Open question to answer first:* is there even a multi-matrix spectral-action model whose 2-cut corresponds to a block-dimension split `2:3`, rather than an eigenvalue-interval split? *Downgrade if:* the single-matrix↔block-split category gap cannot be closed.
2. **Tailored-deformation thread [D].** Characterize the *minimal* explicit symmetry-breaking term (à la Steinacker-Zahn) needed to make `(2,3)` a local — then global — minimum, and state honestly that it is inserted by hand. *Value:* quantifies *how much* external structure `(2,3)` requires; a large requirement is itself an informative (likely negative) result. *Downgrade if:* the term amounts to simply writing the answer in.
3. **Negative-result consolidation [B].** Strengthen and document the *no-go* results (equal-block-only, SUSY→U(1)) as a rigorous statement that single-trace and SUSY routes cannot produce asymmetric `(2,3)`. *This is the most likely durable scientific output of PR-B2* and directly reinforces Appendix B.

## 5. Anti-target-leakage and anti-fabrication discipline (binding)

- No mechanism is coded, simulated, or written up **as if** it produces `(2,3)` before that is demonstrated. The (2,3) target never enters any solver, loss, stopping rule, or initial-condition selection used for a *vacuum search* (a planted IC for a *lifetime* measurement is permitted, as in PR-B1, and never referenced by the detector).
- The arXiv:2601.14141 over-reading is recorded as a cautionary case: **a real citation can still be mis-read; verify the claim, not just the existence of the paper.**
- If a future "deep research" document asserts a verified `(2,3)` mechanism, it is checked against primary text before entering the ledger — and tagged [E]/unverified until the *specific claim* (not merely the source) is confirmed.
- No PASS/SOLVED/breakthrough verdict. The honest endpoint may well be: *no minimal spontaneous deformation produces asymmetric `(2,3)`* — a valid, publishable negative result that sharpens UIDT rather than inflating it.

## 6. Disposition of the conflicting upload documents

- `Symmetriebrechung.txt` and the derivative "Fazit"/"Badewanne" texts: **NOT** entered into the ledger as evidence. If retained, tag **[E] / over-read** with the note that their central claim rests on a category error (2-cut spectrum ≠ Wedderburn block split) refuted by full-text reading of arXiv:2601.14141.
- The five concordant documents (`Seriöser_Research.pdf`, `_A__Zusammenfassung_der_Lösung.md`, `deep-research-report*.md`, `YMCS-Matrixkondensation.txt`): consistent with primary sources; usable as **[D]** literature surveys, flagged for the standard DOI sweep.

## 7. Claims table (delta)

| ID | Claim | Class | Falsification / downgrade |
|---|---|---|---|
| B2-01 | No known mechanism forces stable asymmetric `(2,3)` as global vacuum | [B] (negative, literature-verified) | A primary-source-verified mechanism producing asymmetric `(2,3)` spontaneously |
| B2-02 | Massive Myers gives only **equal-block** `U(k)`, not `(2,3)` | [B] | A massive-deformation parameter window yielding stable unequal `2:3` blocks |
| B2-03 | SUSY worsens the no-go (→`U(1)`) | [B] | A SUSY model stabilizing `k>1` asymmetric blocks |
| B2-04 | arXiv:2601.14141 shows single-matrix 2-cut, **not** a Wedderburn block split | [A] (textual fact, full text read) | A passage in the paper constructing a multi-matrix `M₂⊕M₃` block vacuum |
| B2-05 | Multi-trace / Dirac route is an **open** [D]/[E] thread, not a solution | [D]/[E] | An existence proof selecting asymmetric `(2,3)` as global min |

## 8. Sign-off block

```
PI review of charter scope:                       ____________________  date: ________
Premise accepted ((2,3)-stabilizer UNSOLVED):     [ ] yes
Dirac route recorded as open thread, not solution:[ ] yes
Symmetriebrechung.txt tagged [E]/over-read:       [ ] yes
PR-B2 opened as [D]/[E] programme (not mandate):   [ ] yes
Most-likely output = negative-result consolidation:[ ] acknowledged
```

---

*Drafted by Claude/Opus, advisory capacity. Built on full-text verification of arXiv:2601.14141 and primary-source evidence classes for each candidate. No mechanism is pre-declared as the solution; the (2,3)-stabilizer is recorded as UNSOLVED. This is the honest successor to the PR-B1 null. Authorizes nothing; the PI decides.*

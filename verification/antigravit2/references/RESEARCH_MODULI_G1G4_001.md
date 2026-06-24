# Moduli-Space Formulation of the G1–G4 Profile: A Technical Research Note

| Field | Value |
|---|---|
| Document ID | `RESEARCH-MODULI-G1G4-001` (advisory; for PI review) |
| Status | **[D] — technical research programme. Falsifiable, unconfirmed. Not a closure.** |
| Author | Claude/Opus, advisory capacity. No sign-off/merge/upgrade. |
| Anchoring | Real, established objects: moduli spaces of finite real spectral triples (Ćaćić arXiv:0902.2068); Krajewski diagrams (Krajewski 1998; Paschke–Sitarz 1998); Connes/Chamseddine–Connes classification. |
| Separation | Distinct from the [E] methodology note (`METHODOLOGY-GLBC-001`). This is mathematics, not philosophy; it makes no reality or consciousness claim. |

---

## 1. The question

Can the G1–G4 admissibility profile (multiplicity $\geq 2$; rank $\geq 4$; KO-dimension-6 real structure; chirality) be expressed as a **sub-variety in the moduli space of admissible finite real spectral triples** — and if so, does that formulation *close* the multiplicity-$\geq 2$ gap or merely *relocate* it?

## 2. The established starting point (verified, [A] re: corpus)

The relocation result is already established against primary sources and recorded in the manuscript (`rem:moduli-relocation`):

The moduli space of Dirac operators $\mathcal{D}(A,H,P)$ is defined **only after** fixing the algebra $A$ (with its Wedderburn decomposition), the bimodule $H$ (with its multiplicity matrix), and the structure datum $P$ (including the KO-dimension $n \bmod 8$); only the Dirac operator then varies continuously within that fixed space (Ćaćić, Def. 2.13, 2.16). Therefore:

- **theorem-fixed constraints (input labels):** block dimensions $n_i$, real forms $\mathbb{K}_i \in \{\mathbb{R},\mathbb{C},\mathbb{H}\}$, KO-dimension $n \bmod 8$ — these are G1, G2, G3;
- **free moduli (coordinates):** only the Dirac/Yukawa data.

A sub-variety cut inside a fixed $\mathcal{D}(A,H,P)$ can constrain only the Yukawa coordinates; it cannot generate the discrete labels that *define which moduli space exists*. So: **the formulation relocates the insertion to the discrete index data; it does not close the gap.** This is the verified baseline, not the open question.

## 3. The genuinely open question (the [D] programme)

The relocation is established for the *known* formalism. What is **not** established is whether relocation is **necessary** — i.e. whether *any* reformulation that treats the Yukawa data as moduli must treat the Wedderburn/KO data as constraints. Two precise research targets follow.

### 3.1 Relocation Necessity Conjecture (the central target)

> **Conjecture (RNC).** Let $\mathcal{M}$ be any moduli space of finite real spectral triples in which a continuous family of admissible Dirac operators varies. Then the Wedderburn invariants $\{(n_i,\mathbb{K}_i)\}$ and the KO-dimension $n \bmod 8$ are necessarily discrete invariants of $\mathcal{M}$ (locally constant), not continuous coordinates. Equivalently: no admissible continuous deformation within a connected component of $\mathcal{M}$ changes the block partition, the real forms, or the KO-dimension.

If RNC is **true**, the relocation is a theorem, not an artifact of one formalism: the multiplicity gap *cannot* be closed by any moduli-space reformulation, and the lower bounds on $\mathcal{A}$ (Cor. on admissible algebras) acquire the status of *provably necessary* insertions rather than *currently unknown* ones. This would be a genuine, publishable structural result — a no-go on a whole class of attempted closures.

If RNC is **false**, there exists a moduli space with a continuous path changing a Wedderburn invariant or the KO-dimension — which would itself be a striking and publishable object, and would reopen the question of endogenous generation.

**Falsification / downgrade.** RNC is falsified by exhibiting one admissible continuous deformation that changes a discrete label. It is supported (not proved) by each formalism in which the labels are shown locally constant. It is downgraded to [E] if it cannot be given a precise enough statement to be tested.

### 3.2 What a proof of RNC would require (necessary conditions, stated honestly)

A proof would need to establish, for the relevant category of finite real spectral triples:
1. that the multiplicity matrix $V_{ij}$ is a *discrete* invariant under admissible continuous Dirac deformations (plausible from Ćaćić's monoid-isomorphism $m \mapsto [H_m]$, Prop. 3.1, but the *continuity* statement must be made precise);
2. that the KO-dimension cannot change continuously (plausible from its definition via the discrete sign triple $(\varepsilon,\varepsilon',\varepsilon'')$, but again the deformation statement is what is needed);
3. that the real forms $\mathbb{R}/\mathbb{C}/\mathbb{H}$ are rigid under such deformations (Wedderburn–Artin rigidity of the algebra type).

Items 1–3 are individually plausible and partly implicit in the existing classification, but **assembling them into a deformation-rigidity theorem is the actual mathematical work** and is not done here. This note states the target and its necessary conditions; it does not claim the theorem.

## 4. Why this is the natural successor to the gap analysis

The gap analysis established *that* the insertion is currently unavoidable. RNC asks whether it is *necessarily* unavoidable. This is the difference between "no known mechanism" (current corpus) and "no possible mechanism in this class" (a theorem) — exactly the upgrade from a survey result to a structural one. It is also the most publishable direction, because a deformation-rigidity theorem for the discrete invariants of finite real spectral triples would be of interest to the NCG community independent of UIDT.

## 5. Relation to dynamical-selection programmes

The Dirac-ensemble / FRGE programme (Pérez-Sánchez 2021; Khalkhali–Pagliaroli) makes the Dirac operator dynamical and exhibits phase transitions. RNC is *consistent* with and *complementary* to that programme: even a fully dynamical selection of the Dirac/Yukawa coordinates would, if RNC holds, operate **within** a fixed label set — it could select Yukawa structure but not generate the Wedderburn/KO data. So RNC, if proved, would sharply delimit what any dynamical-selection result could claim. This is a concrete, testable interaction between the two research lines.

## 6. Claims table

| # | Claim | Class | Falsification / downgrade |
|---|---|---|---|
| MOD-01 | In the known formalism, the moduli space is defined only after fixing $A,H,P$; labels are constraints, Yukawa data are coordinates | [A] re: corpus | A primary source defining the moduli space with continuous Wedderburn/KO coordinates |
| MOD-02 | A sub-variety formulation relocates the multiplicity gap; it does not close it | [A] re: corpus | A construction generating the discrete labels from within a fixed moduli space |
| MOD-03 | Relocation Necessity Conjecture: discrete labels are locally constant in any such moduli space | [D] | One admissible continuous deformation changing a discrete label |
| MOD-04 | A proof of RNC would upgrade the lower bounds on $\mathcal{A}$ from "currently unknown" to "provably necessary" insertions | [D] | RNC shown false |
| MOD-05 | RNC, if true, delimits any dynamical-selection result to a fixed label set | [D] | A dynamical mechanism shown to change a discrete label |

## 7. Reproduction note

The established claims (MOD-01, MOD-02) are textual/structural and require no numerics; they are sourced to Ćaćić (arXiv:0902.2068, Defs. 2.13/2.16, Thm. 2.2, Prop. 3.1). The conjectural claims (MOD-03–05) are stated as targets with explicit falsification conditions; no result is asserted as proved.

---

*Drafted by Claude/Opus, advisory capacity. The relocation result is established; the Relocation Necessity Conjecture is an open [D] target with stated necessary conditions, not a theorem. This note makes no reality or consciousness claim and is separate from the [E] methodology note. Authorizes nothing; the PI decides whether to pursue it.*

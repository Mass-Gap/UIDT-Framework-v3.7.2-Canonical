# PATCH_DRAFT — Appendix Addendum: Gap Localization for $S(x)\to\mathcal{A}\to G_{\mathrm{SM}}$ and the Status of Candidate Algebras

| Field | Value |
|---|---|
| Patch ID | `PATCH-APP-GSM-GAP-001` (DRAFT for PI review) |
| Target | New subsection/addendum to the Non-Derivability appendix of UIDT Ontology v3.9.9 (extends the existing Appendix A material: Singlet Rigidity, Discrete Exactness, Single-Mode Rigidity, Abelianization Barrier, Rank-Budget, Wedderburn Moduli, Gap Localization) |
| Author | Claude/Opus, advisory capacity. **No merge authorization.** PI decides inclusion. |
| Evidence ceiling | [A] for the theorem-level rigidity/gap results (statements about the current theorem corpus); [D] for the division-algebra candidate; nothing upgrades ONT-08. |
| Status | Repository-grade English. All references individually verifiable; division-algebra primary sources fetched/read this session. |

---

## A.X Gap Localization and the Status of Candidate Intermediate Algebras

### A.X.1 Summary of the obstruction (theorem-level, [A] re: current corpus)

For the primitive $(\Gamma, S\!:\!V\to\mathbb{R})$ with symmetries implemented by canonical linear transformations, no gapless ab initio derivation $S(x)\to G_{\mathrm{SM}}$ exists within established theorems. The obstruction is localized to a single step — the enlargement of the abelian single-mode local algebra to a noncommutative algebra of local multiplicity $\geq 2$ — and is quantified by four conditions that **no known mechanism satisfies jointly**:

- **(G1)** fiber-multiplicity generation $1\to n\geq 2$ without inserted variables — blocked homologically (Abelianization Barrier: any loop-phase assignment factors through $H_1(\Gamma)=\pi_1(\Gamma)^{\mathrm{ab}}$, bracket $\equiv 0$) and algebraically (a scalar-generated algebra is commutative; $\mathrm{Inn}(\mathcal{A})=\{1\}$);
- **(G2)** theorem-determined Wedderburn invariants $\{(1,\mathbb{C}),(1,\mathbb{H}),(3,\mathbb{C})\}$ — currently free moduli (matrix dimension $N$, block partition, and real forms $\mathbb{R}/\mathbb{C}/\mathbb{H}$ are unconstrained; gauge structure is the automorphism shadow $\mathrm{Aut}(M_N(\mathbb{C}))=PU(N)$ of the *inserted* algebra, Skolem–Noether);
- **(G3)** an endogenous real structure $J$ of KO-dimension 6 — currently a choice (the Chamseddine–Connes axiom, external to any scalar input);
- **(G4)** chirality-capable matter — blocked by Nielsen–Ninomiya for local translation-invariant lattices; no established non-abelian chiral construction with SM content.

The unique established endogenous enhancement of a single scalar to a non-abelian current algebra (Frenkel–Kac $\widehat{\mathfrak{su}}(2)_1$) satisfies a weakened (G1) **only** in $1{+}1$D, under target compactification and radius tuning, and is bounded by the Rank-Budget Lemma at $\mathrm{rank}=1$ against the requirement $\mathrm{rank}(\mathfrak{g}_{\mathrm{SM}})=4$.

**Consequence.** $G_{\mathrm{SM}}$ is, on every known route, **selected, not forced**. This is consistent with — and sharpens — the manuscript's canonical posture (gauge sector coupled, not generated; $S(x)\to\mathcal{A}\to G_{\mathrm{SM}}$ at [D]). It is a gap-localization, **not** an impossibility theorem for all conceivable enriched routes; no such theorem exists.

### A.X.2 Lower bounds on any admissible $\mathcal{A}$ (Corollary, [A]/[D])

Any candidate intermediate algebra $\mathcal{A}$ must carry: local multiplicity $\geq 2$ (non-abelian fiber); rank resources $\geq 4$; a real structure with $J^2$-signs of KO-dimension 6; and a chirality mechanism evading the Nielsen–Ninomiya / finite-2-group obstructions. **Any candidate failing one bound is excluded before dynamical analysis.** These bounds are the constructive yield of the gap analysis: they tell a model-builder what $\mathcal{A}$ must minimally contain.

### A.X.3 The division-algebra programme as a [D] candidate for $\mathcal{A}$

A substantial peer-reviewed programme constructs SM structure from the normed division algebras $\mathbb{R},\mathbb{C},\mathbb{H},\mathbb{O}$ and their multiplication (Clifford) algebras [Dixon, Furey, Dubois-Violette–Todorov, Gresnigt]. It is the strongest existing source of a *principled* reason for the specific factors of $\mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C})$ — and is recorded here as a candidate for $\mathcal{A}$, at evidence class **[D]**, with its limits stated as the primary sources themselves state them.

**What the programme establishes (verified, primary sources read):**
- One generation of SM Weyl representations arises as a single copy of $\mathbb{R}\otimes\mathbb{C}\otimes\mathbb{H}\otimes\mathbb{O}$ acting on itself (Furey–Hughes, Phys. Lett. B 827 (2022) 136959); $SU(3)_C\times U(1)_{em}$ arises from $\mathbb{C}\ell(6)$ minimal left ideals, weak $SU(2)$ from $\mathbb{C}\ell(4)$ [Furey, Eur. Phys. J. C 78 (2018) 375].
- $G_{\mathrm{SM}}$-related gauge structure appears as the **stabilizer / automorphism** structure of a rigid algebra: e.g. $G_2=\mathrm{Aut}(\mathbb{O})$ has $SU(3)$ as the stabilizer of an imaginary unit (Günaydin–Gürsey, J. Math. Phys. 14 (1973)); the exceptional Jordan algebra $J_3(\mathbb{O})$ route (Dubois-Violette–Todorov, Int. J. Mod. Phys. A 33 (2018) 1850118).

**What the programme does NOT establish (stated by its own authors — the honest bound):**
1. **Selection is by inserted substructure, not derivation.** The gauge group is obtained by *restricting* to symmetries preserving a chosen subalgebra. Explicitly (Gourlay–Gresnigt, arXiv:2407.01580): a $\mathbb{C}\ell(8)$ minimal left ideal is invariant under $SU(4)$; restricting to the symmetry preserving a $\mathbb{C}\ell(2)$ (quaternionic) substructure breaks it to the maximal subgroup $SU(3)\times U(1)$. The quaternionic structure is **inserted**, not generated — the same move as (G2)/(G3).
2. **Three generations remain unsolved.** "An algebraic foundation for the existence of three generations within the division algebraic framework remains elusive" (ibid.); the popular GUTs ($SU(5)$, $SO(10)$, Pati–Salam) are likewise single-generation. Generations are introduced via an inserted discrete symmetry (e.g. $S_3=\mathrm{Aut}(\mathbb{S})/\mathrm{Aut}(\mathbb{O})$), and anomaly cancellation is flagged as future work (Furey, Annalen der Physik 2025).
3. **The primitive is an algebra, not a scalar.** The starting datum is $\mathbb{R}\otimes\mathbb{C}\otimes\mathbb{H}\otimes\mathbb{O}$ (or $\mathbb{C}\ell(n)$), a rich structure. No construction in this programme begins from a single real scalar field; it presupposes the multiplicity that (G1) identifies as the unavoidable insertion.

**Status assignment.** The division-algebra programme is a verified, active, peer-reviewed **[D] candidate for $\mathcal{A}$**. It illustrates Cor. A.X.2 by *exhibiting* the inserted structure the gap analysis predicts as necessary (it supplies multiplicity, a real/quaternionic structure, and rank), and it is the best available *principled* motivation for the SM factors. It does **not** rescue scalar primitivity, does **not** uniquely derive $G_{\mathrm{SM}}$ (group emerges via inserted stabilizer choice), and does **not** account for three generations or chirality anomaly cancellation from first principles. Any UIDT use of it must carry these three bounds explicitly.

### A.X.4 Forbidden inferences (binding)

- Mechanism relevance is not framework validation. Neither the string-net, NCG, matrix-model, nor division-algebra literature supports a claim that UIDT *derives* $G_{\mathrm{SM}}$.
- The division-algebra programme must not be cited as a "verified mechanism" for unique $G_{\mathrm{SM}}$ selection; its own authors record the selection as stabilizer-conditional and the three-generation question as open.
- This addendum upgrades nothing: ONT-08 stays [D]; $S(x)\to\mathcal{A}\to G_{\mathrm{SM}}$ stays [D]; no constant or claim is promoted.

### A.X.5 Claims table (delta)

| # | Claim | Class | Falsification / downgrade |
|---|---|---|---|
| GAP-01 | No gapless ab initio $S(x)\to G_{\mathrm{SM}}$ in current corpus | [A] re: corpus | A theorem generating a noncommutative $\mathcal{A}$ endogenously from single-boson data |
| GAP-02 | Obstruction localized to multiplicity-$\geq2$ insertion; conditions G1–G4 | [A] | A mechanism satisfying G1–G4 jointly |
| GAP-03 | Lower bounds on $\mathcal{A}$ (mult $\geq2$, rank $\geq4$, $J$ KO-dim 6, chirality) | [A]/[D] | A dynamical theorem fixing Wedderburn invariants and $J$ endogenously |
| GAP-04 | Division-algebra programme is a [D] candidate for $\mathcal{A}$; group via inserted stabilizer, 3 generations open | [D] | Primary-source-verified unique $G_{\mathrm{SM}}$ derivation + spontaneous 3 generations from the algebra alone |
| GAP-05 | Division-algebra route does not begin from a scalar; presupposes multiplicity | [A] (textual fact) | A construction in this programme starting from a single real scalar |

### A.X.6 Reproduction note

Symbolic/theorem-level results require no numerics: the rigidity lemmas are representation-theoretic identities ($GL(1,\mathbb{R})$ max compact $\{\pm1\}$; $H_1=\pi_1^{\mathrm{ab}}$; Skolem–Noether $\mathrm{Aut}(M_N)=PU(N)$; rank-budget for level-1 simply-laced affine algebras). The division-algebra claims are sourced to the cited primary literature, fetched and read.

### A.X.7 DOI / reference check (flagged for the standard sweep)

- Furey–Hughes, Phys. Lett. B 827 (2022) 136959 — DOI 10.1016/j.physletb.2022.136959.
- Furey, Eur. Phys. J. C 78 (2018) 375 — DOI 10.1140/epjc/s10052-018-5844-7.
- Furey, Phys. Lett. B 785 (2018) 84 — DOI 10.1016/j.physletb.2018.08.032.
- Dubois-Violette–Todorov, Int. J. Mod. Phys. A 33 (2018) 1850118.
- Günaydin–Gürsey, J. Math. Phys. 14 (1973) 1651.
- Gourlay–Gresnigt, arXiv:2407.01580 (full text read this session).
- Furey, Annalen der Physik (2025), DOI 10.1002/andp.202500229.
- (Plus the Track-1/2 references already in the appendix: Levin–Wen, Lan–Kong–Wen, Nielsen–Ninomiya, Chamseddine–Connes, Frenkel–Kac, Skolem–Noether, Steinacker.)

---

*Drafted by Claude/Opus, advisory capacity. The gap-localization and lower-bound results are theorem-level; the division-algebra programme is recorded as a verified [D] candidate for $\mathcal{A}$, bounded exactly as its own primary sources bound it. No mechanism is presented as a solution; the $(2,3)$/Wedderburn selection and the scalar-to-algebra step remain open. Authorizes nothing; the PI decides inclusion.*

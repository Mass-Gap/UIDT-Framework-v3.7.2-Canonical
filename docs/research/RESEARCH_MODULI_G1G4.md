# Phase 9: G1-G4 Moduli Program & RNC
**Epistemic Status:** [D] — Research note. Contains conjectures and moduli program outlines.

## 1. The Noncommutative Moduli Space
A point in the noncommutative moduli space $\mathcal{D}_{A,H,P}$ is specified by:
- **Wedderburn Data ($A$):** The partition structure of the finite algebra (e.g., $M_3(\mathbb{C}) \oplus M_2(\mathbb{C}) \oplus \mathbb{C}$ for `[3,2,1]`).
- **Hilbert Space ($H$):** A bimodular representation encoding the fermion multiplicities.
- **Dirac Operator ($D$) and Structure ($P$):** The metric dimension and KO-dimension signatures.

## 2. Relocation Necessity Conjecture (RNC)
**Statement:** Discrete topological invariants—specifically the block sizes $n_i$, the KO-dimension, and the multiplicity matrix $K_i$—are locally constant under any *admissible* continuous deformation of the Dirac operator.

**Significance:** If true, the discrete structure of the fermion sectors cannot "smoothly decay" into a different partition without passing through a non-admissible singularity (where spectral triple axioms fail).

**Falsification:** To falsify RNC, one must construct a smooth 1-parameter family of Dirac operators $D(t)$ that continuously connects two non-isomorphic Wedderburn structures (e.g. from `[4,2]` to `[3,2,1]`) while satisfying all spectral triple axioms at every $t$.

## 3. G1-G4 Insertions
Conditioned on RNC, the generations G1, G2, G3 and the sterile sector G4 appear as *provably necessary structural insertions* to maintain intersection-form non-degeneracy and anomaly cancellation across the moduli space.
They are not ad-hoc additions but required topological boundaries.

## 4. Gap Analysis
**Proven:**
- Wedderburn decomposition of finite C*-algebras (standard math).
- Exhaustive elimination at $N=6$ isolates `[3,2,1]` under H1/H2 (Phase 9 Lean proof).

**Conjecture / Open Gaps:**
- The RNC remains an unproven topological claim.
- Global minimization of the Dirac action yielding exactly $N=6$ as the stable ground state is hypothesized but not proven. (Current numerical work assumes $N=6$ as a phenomenological boundary).

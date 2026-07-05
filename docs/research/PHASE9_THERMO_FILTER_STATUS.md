# Phase 9: Matrix Thermodynamics Filter Status
**Epistemic Status:** [D] — Numerical audit & algebraic identities. No new physical claims.

## 1. Thermodynamic Kernel
The core thermodynamic identity proven in `BlockPartition.lean` is:
$$N^2 = S + 2U_{\text{off}}$$
**Status:** [A] (Checked Identity). This holds algebraically for any integer partition.

## 2. NCG Filters
To isolate specific partitions (e.g. `[3,2,1]` for $N=6$), we introduce two filters:

### H1: Intersection-Form Filter
**Definition:** Consecutive block sizes in a sorted partition differ by at most 1.
**Status:** [DESIGN-LEVEL]. Motivated by intersection-form non-degeneracy in NCG (e.g. Chamseddine-Connes-Marcolli), but not formally derived from first principles here.

### H2: Mass Non-Degeneracy Filter
**Definition:** The partition has at least two blocks, and no block size is repeated.
**Status:** [HEURISTIC]. Motivated by the physical observation that fermion generations do not have degenerate masses (which would arise from algebraically indistinguishable blocks).

## 3. Elimination at N=6

The thermodynamic kernel with block condensation, $S=\sum n_i^2$, and the off-diagonal penalty is conceptually very strong and compatible with both the IKKT/BFSS intuition and the existing UIDT baseline. The sensitive points, however, are precisely those that must be explicitly marked here as assumptions: Filter 1 (the intersection constraint $n_i - n_j \le 1$) is not yet a theorem in this generality; Filter 2 (mass non-degeneracy) currently functions more as a dynamical plausibility argument than a proven theorem; and the global uniqueness of `[3,2,1]`, as well as the assertion that larger $N$ inevitably fragment into `[3,2,1]` subgraphs, extends beyond what is presently mathematically secured.

In the following, the result is therefore formulated as an elimination argument under explicit hypotheses, rather than as an unconditional theorem.

**Proposition ($N=6$).** Under hypotheses H1 and H2, `[3,2,1]` is the unique thermodynamically and topologically admissible partition of $N=6$.
**Status:** [D] (Formalized in `EliminationN6.lean`).
All 10 rival partitions are explicitly eliminated.
- **Falsification Path:** If H1 or H2 is weakened, uniqueness is lost (e.g., `[4,2]` becomes admissible if H1 is dropped; `[2,2,1,1]` if H2 is dropped).

## 4. Uniqueness Conjecture (Staircase)
**Conjecture:** For general $N$, the admissible partitions under H1 and H2 are uniquely staircase-type components $[k, k-1, \dots, 1]$ where $k(k+1)/2 = N$.
**Status:** [D]. Verified for $N=6$. Open for arbitrary $N$.

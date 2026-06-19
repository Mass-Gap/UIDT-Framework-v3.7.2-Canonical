# PR-B0 Preflight Protocol: Observable Injectivity, Candidate Set Reduction & Deterministic Detection

## 1. Physical Motivation & Findings

### 1.1 Non-Injectivity of the Casimir Observable
The Casimir observable \( Q = \sum_{a=1}^3 X_a^2 \) is strictly non-injective for spin-0 blocks (\( n=1 \)) and vacuum padding. Both yield \( Q = 0 \) on the classical background and acquire indistinguishable \( \mathcal{O}(\epsilon^2) \) noise profiles. Attempting to differentiate a dynamical \( n=1 \) block from vacuum zero-modes using solely the eigenvalues of \( Q \) leads to a fundamentally ill-posed detection task. 

Introducing a fluctuation-coupling observable to save the \( 1 \)-blocks would require ad-hoc thermodynamic assumptions about "light" vs. "heavy" bifundamental modes, violating the mathematical determinism of the UIDT Framework.

### 1.2 Structural Failure of the KDE Mechanism
Even upon restricting the candidate set to positive-spin equivalence classes, the previously frozen Silverman-KDE peak-counting mechanism exhibits structural instability across the N-ladder. The \( \alpha^2 \)-scaling of the noise drives the global bandwidth in a way that inherently shatters and merges eigenvalue clusters (hit rates of 0.0 - 0.6). A purely statistical mechanism (KDE) is inappropriate for a strictly algebraic observable spectrum.

## 2. Decision & Protocol

We formally declare the \( n=1 \) block **unobservable** under the pure \( Q \)-spectrum and **abandon the KDE peak-counting detector**. The candidate set and detection mechanism must be fully cleaned and frozen prior to PR-B1-002.

### 2.1 Candidate Set Reduction
All partitions containing `1` are projected to their positive-spin equivalence classes. The candidate set must be completely \( Q \)-injective.
- `[1:2:3]` \( \to \) `(2,3)`
- `[1:1]` \( \to \) `[Vakuum/Padding]` (Removed as a distinct thermodynamic phase)
- `[1:1:2:3]` \( \to \) `(2,3)`

**Critical Implication for PR-B1:** The original hypothesis `[1:2:3]` no longer exists as a testable class under the conservative route. PR-B1-002 will test the rigorously well-posed hypothesis: *"Does the model condense into the positive-spin ratio class 2:3?"*

### 2.2 The Deterministic Grid-Assignment Detector
The KDE mechanism is replaced by a strict, algebraic projection detector:
1. The allowed Casimir levels form a known, finite grid: \( Q_n = \alpha^2 \frac{n^2 - 1}{4} \).
2. The detector maps each eigenvalue to the nearest valid grid level, subject to a fixed, class-symmetric tolerance \( \tau \).
3. Degenerate blocks are strictly counted by eigenvalue multiplicity divided by block dimension. No density estimation is performed.

### 2.3 PR-B0 Validation Gate
Before PR-B1-002 can commence, PR-B0 must analytically prove that the Deterministic Grid-Assignment Detector achieves \( \ge 95\% \) recovery on the collapsed, positive-spin candidate set across the full N-ladder (\( N \in \{16, 24, 32, 48, 64\} \)). 
The calibration of the single scalar parameter \( \tau \) must be strictly evaluated and frozen as a successful gate outcome within PR-B0.

## 3. Next Steps
1. Abort the current `feature/prb1-pilot-ag-sim` PR merge. The codebase will not be patched with ad-hoc bandwidth fixes.
2. Implement PR-B0 to build the Grid-Assignment Detector, perform the \( \tau \) calibration, and prove \( \ge 95\% \) separability.
3. Proceed to PR-B1-002 only upon successful completion of PR-B0.

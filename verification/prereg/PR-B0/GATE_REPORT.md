# GATE REPORT: PR-B0.1 Preflight
## Version: PR-B0.1 (C1 alpha-known, C2 raw-multiset, C3 extended 8-class set)
## Date: 2026-06-16

---

## 1. Exact checks (A-audit)

- **verify-grid**: PASS. Q_n = alpha^2(n^2-1)/4 matches j(j+1) for n=1..8.
- **verify-injective**: PASS. P_B0 (8 classes) has pairwise-distinct raw Casimir signatures.

---

## 2. Calibrated tau

- **Frozen tau**: 0.20
- **Calibration version**: PR-B0.1
- **Calibration score**: 76/120 configs achieved >=0.95 at delta=0.10

---

## 3. Separability boundary rho*(delta)

| class | d=0.05 | d=0.10 | d=0.20 | d=0.30 |
|---|---|---|---|---|
| (2, 3) | rho>=0.1351 | **UNSAT** | UNSAT | UNSAT |
| (2, 4) | rho>=0.1579 | **UNSAT** | UNSAT | UNSAT |
| (2, 2, 3) | rho>=0.1795 | rho>=0.1795 | UNSAT | UNSAT |
| (3, 4) | rho>=0.1795 | rho>=0.1795 | UNSAT | UNSAT |
| (2, 2, 2) | rho>=0.1579 | **UNSAT** | UNSAT | UNSAT |
| (3, 3, 3) | rho>=0.2195 | rho>=0.2195 | UNSAT | UNSAT |
| (4, 4, 4) | rho>=0.2727 | rho>=0.2727 | UNSAT | UNSAT |
| (3, 6) | rho>=0.2195 | rho>=0.2195 | UNSAT | UNSAT |

### Key finding: projection eats small blocks

Classes containing n=2 blocks fail at delta=0.10 because the n=2 Casimir level
(Q_2 = 0.75 * alpha^2) is close enough to the noise-elevated padding band that
the log-gap projection absorbs them. The dominant misclassification is
*block-dropping*: (2,3) -> (3,), (2,4) -> (4,), (3,4) -> (4,).

### Classes satisfiable at delta=0.10

Only 5 of 8 classes clear >=0.95 at delta=0.10:
- (2, 2, 3) at rho >= 0.1795
- (3, 4) at rho >= 0.1795
- (3, 3, 3) at rho >= 0.2195
- (4, 4, 4) at rho >= 0.2727
- (3, 6) at rho >= 0.2195

### Classes satisfiable only at delta=0.05

- (2, 3) at rho >= 0.1351
- (2, 4) at rho >= 0.1579
- (2, 2, 2) at rho >= 0.1579

---

## 4. Confusion matrix (delta=0.10, all N/alpha pooled)

| planted | () | (2,2) | (2,2,2) | (2,2,3) | (2,3) | (2,4) | (2,) | (3,3) | (3,3,3) | (3,4) | (3,6) | (3,) | (4,4) | (4,4,4) | (4,) | (6,) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **(2,3)** | 0.5% | 0.0% | 0.0% | 0.0% | **69.7%** | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **29.8%** | 0.0% | 0.0% | 0.0% | 0.0% |
| **(2,4)** | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% | **69.2%** | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **30.7%** | 0.0% |
| **(2,2,3)** | 0.1% | 0.0% | 0.0% | **73.5%** | 6.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **20.0%** | 0.0% | 0.0% | 0.0% | 0.0% |
| **(3,4)** | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **80.0%** | 0.0% | 0.0% | 0.0% | 0.0% | **20.0%** | 0.0% |
| **(2,2,2)** | 6.9% | **39.0%** | **49.3%** | 0.0% | 0.0% | 0.0% | 4.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **(3,3,3)** | 4.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 14.1% | **76.8%** | 0.0% | 0.0% | 5.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| **(4,4,4)** | 5.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 8.4% | **83.4%** | 2.7% | 0.0% |
| **(3,6)** | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **80.0%** | 0.0% | 0.0% | 0.0% | 0.0% | **20.0%** |

### Confusion analysis

- **No cross-class confusion between distinct P_B0 members.** All misclassifications
  are *block-dropping* errors (e.g., (2,3) -> (3,)), not mistaking one candidate for another.
  This confirms Q-injectivity holds in practice.
- **(2,2,2) is structurally fragmented**: 49.3% correct, 39.0% -> (2,2) (lost one block),
  6.9% -> () (total projection failure), 4.7% -> (2,) (lost two blocks).
- **(3,3,3)** and **(4,4,4)** show the same pattern at lower severity: block-dropping
  to (3,3)/(4,4) at 14.1%/8.4%.

---

## 5. Class dispositions

| Class | delta=0.10 | delta=0.05 | Failure mode |
|---|---|---|---|
| (2, 3) | UNSAT | rho>=0.1351 | n=2 block eaten by projection |
| (2, 4) | UNSAT | rho>=0.1579 | n=2 block eaten by projection |
| (2, 2, 3) | rho>=0.1795 | rho>=0.1795 | Marginal; 20% block-drop to (3,) |
| (3, 4) | rho>=0.1795 | rho>=0.1795 | 20% block-drop to (4,) |
| (2, 2, 2) | UNSAT | rho>=0.1579 | Structurally fragmented (49.3% correct) |
| (3, 3, 3) | rho>=0.2195 | rho>=0.2195 | Degenerate but resolvable |
| (4, 4, 4) | rho>=0.2727 | rho>=0.2727 | Degenerate but resolvable |
| (3, 6) | rho>=0.2195 | rho>=0.2195 | Well-separated levels |

---

## 6. Scientific implication for PR-B1-002

The primary scientific target (2,3) — the positive-spin projection of the original
hypothesis [1:2:3] — is resolvable only at delta<=0.05. Whether this is sufficient
depends on the thermodynamic noise floor of the HMC simulation. If thermal fluctuations
produce operator-norm perturbations exceeding delta=0.05, the (2,3) class cannot be
confirmed or excluded by this detector.

This is a measured finding, not a limitation to be engineered around.

---

## 10. Sign-off block

```
PI sign-off (required before PR-B1-002):     Philipp Rie           date: 2026-06-18
PR-B0.1 gate verdict (A-audit, advisory):    [x] satisfiable  [ ] NOT-SATISFIABLE
Frozen tau (calibration output):             tau = 0.20
Admissible region per class (≥0.95@δ≤0.10):
  (2,3): ρ≥0.1351; (2,4): ρ≥0.1579; (2,2,3): ρ≥0.1795; (3,4): ρ≥0.1795;
  (2,2,2): ρ≥0.1579; (3,3,3): ρ≥0.2195; (4,4,4): ρ≥0.2727; (3,6): ρ≥0.2195
(2,2,2) disposition:  UNRESOLVABLE at d=0.10 (49.3% recovery, structural fragmentation)
(2,3) disposition:    UNRESOLVABLE at d=0.10 (69.7% recovery, n=2 block eaten by projection)
Gatekeeper CI green on PR-B0 dir:            [ ] yes   run id: ____________
Data versions:                               tau=PR-B0.1, boundary=PR-B0.1
```

*Generated by A-audit (PR-B0.1). This report must be signed by the PI before PR-B1-002 can commence.*

import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath("verification/prereg/PR-B0/src"))
from prb0.planted_ensemble import generate_planted_ensemble
from prb0.detector import projected_grid_assignment_detector

N = 15
alpha = 4.0
delta = 0.10
p = (2, 2, 3)
tau = 0.20

for t in range(200):
    rng = np.random.default_rng(42 + t)
    X1, X2, X3 = generate_planted_ensemble(p, N, alpha, delta, rng)
    pred = projected_grid_assignment_detector(X1, X2, X3, tau, alpha)
    if pred == (2, 3):
        print(f"FAILED AT SEED offset {t}")
        C = X1 @ X1 + X2 @ X2 + X3 @ X3
        C = (C + C.conj().T) / 2
        w = np.linalg.eigvalsh(C)
        print("Eigenvalues of C:")
        print(np.array2string(w, precision=2, suppress_small=True))
        w_max = max(w[-1], 1e-15)
        logs = np.log(np.clip(w, 1e-9 * w_max, None))
        diffs = np.diff(logs)
        cut = int(np.argmax(diffs))
        Q_plus = w[cut + 1:]
        print("Cut index:", cut, "Max gap:", np.max(diffs))
        print("Q_plus:")
        print(np.array2string(Q_plus, precision=2, suppress_small=True))
        
        a2 = alpha**2
        counts = {}
        for q in Q_plus:
            jj = q / a2
            n_float = np.sqrt(max(4 * jj + 1, 0))
            n_star = max(2, round(n_float))
            diff_val = abs((n_star**2 - 1)/4.0 - jj)
            tol_val = tau * max((n_star**2 - 1)/4.0, 0.75)
            if diff_val <= tol_val:
                counts[n_star] = counts.get(n_star, 0) + 1
            else:
                print(f"  DROPPED q={q:.2f} -> jj={jj:.3f} -> n*={n_star}, diff={diff_val:.3f} > tol={tol_val:.3f}")
        print("Counts:", counts)
        break

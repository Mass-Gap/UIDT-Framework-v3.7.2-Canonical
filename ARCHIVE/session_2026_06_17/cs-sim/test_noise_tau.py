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

for tau in [0.12, 0.20]:
    correct = 0
    leak = 0
    for t in range(200):
        rng = np.random.default_rng(42 + t)
        X1, X2, X3 = generate_planted_ensemble(p, N, alpha, delta, rng)
        pred = projected_grid_assignment_detector(X1, X2, X3, tau, alpha)
        if pred == p:
            correct += 1
        elif pred == (2, 3):
            leak += 1
    print(f"tau={tau}: Correct: {correct}/200 ({correct/200*100:.1f}%), Leak: {leak}/200 ({leak/200*100:.1f}%)")

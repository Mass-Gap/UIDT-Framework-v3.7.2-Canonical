import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath("verification/prereg/PR-B0/src"))

from prb0.planted_ensemble import generate_planted_ensemble
from prb0.detector import projected_grid_assignment_detector

rng = np.random.default_rng(42)
N = 15
alpha = 4.0
delta = 0.10
p = (2, 2, 3)

correct = 0
leak = 0
for _ in range(200):
    X1, X2, X3 = generate_planted_ensemble(p, N, alpha, delta, rng)
    pred = projected_grid_assignment_detector(X1, X2, X3, 0.20, alpha)
    if pred == p:
        correct += 1
    elif pred == (2, 3):
        leak += 1

print(f"p={p}, N={N}, alpha={alpha}, delta={delta}")
print(f"Correct: {correct}/200 ({correct/200*100:.1f}%)")
print(f"Leak to (2,3): {leak}/200 ({leak/200*100:.1f}%)")

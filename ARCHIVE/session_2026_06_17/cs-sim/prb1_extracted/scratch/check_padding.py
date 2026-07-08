import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from verification.prereg.PR_B1.eval.validation import _planted_sample
from verification.prereg.PR_B1.eval.detector import eigenvalues_of_Q

rng = np.random.default_rng(42)

for eps in [0.01, 0.1, 0.2]:
    X1, X2, X3 = _planted_sample((1, 2, 3), 16, eps, rng)
    eigs = eigenvalues_of_Q(X1, X2, X3)
    print(f"Eps = {eps}")
    print("Eigenvalues:", np.round(eigs, 2))

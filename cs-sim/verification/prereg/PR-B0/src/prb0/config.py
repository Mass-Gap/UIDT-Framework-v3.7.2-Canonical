import hashlib

# PR-B0.1 Collapsed candidate set (Q-injective; frozen)
# Extended with collision partners for confusion matrix verification.
P_B0 = [
    (2, 3),       # original
    (2, 4),       # original
    (2, 2, 3),    # original
    (3, 4),       # original
    (2, 2, 2),    # degenerate stress case
    (3, 3, 3),    # collision partner for (2,2,2) under gcd-reduction
    (4, 4, 4),    # collision partner for (2,2,2) under gcd-reduction
    (3, 6),       # collision partner for (2,4) under gcd-reduction
]

# Planted noise sweep
DELTA_SWEEP = [0.05, 0.10, 0.20, 0.30]

# Production grid
N_OFFSETS = [0, 4, 8, 16, 32]
ALPHAS = [1.0, 2.0, 4.0]
TRIALS_PER_CELL = 200

def get_deterministic_seed(class_str: str, N: int, alpha: float, delta: float, trial: int) -> int:
    """
    Deterministic seed per (class, N, alpha, delta, trial).
    PR-B0.1 version — seed string includes version tag to prevent cache reuse.
    """
    seed_str = f"PR-B0.1-001|{class_str}|{N}|{alpha}|{delta}|{trial}"
    return int(hashlib.sha256(seed_str.encode('utf-8')).hexdigest()[:16], 16)

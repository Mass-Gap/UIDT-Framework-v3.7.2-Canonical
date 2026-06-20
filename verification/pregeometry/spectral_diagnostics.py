"""Spectral graph diagnostics for PR-2.

Scientific status: [D] (Software graph diagnostic only).
Physical interpretation is strictly forbidden.
"""

from mpmath import mp, matrix, eig, log
from typing import List
from verification.pregeometry.primitives import RelationalState

# Rule 1 compliance: local precision initialization
mp.dps = 80

def _get_adjacency_matrix(state: RelationalState) -> matrix:
    n = state.distinction_count()
    A = matrix(n, n)
    for relation in state.relations:
        i = relation.source.value
        j = relation.target.value
        A[i, j] += 1
        if not relation.directed:
            A[j, i] += 1
    return A

def _get_degree_matrix(state: RelationalState, A: matrix) -> matrix:
    n = state.distinction_count()
    D = matrix(n, n)
    for i in range(n):
        D[i, i] = sum(A[i, j] for j in range(n))
    return D

def combinatorial_laplacian_spectrum(state: RelationalState) -> List[mp.mpf]:
    if state.distinction_count() == 0:
        return []
    A = _get_adjacency_matrix(state)
    D = _get_degree_matrix(state, A)
    L = D - A
    E, _ = eig(L)
    return sorted([mp.re(val) for val in E])

def compute_spectral_gap(eigenvalues: List[mp.mpf]) -> mp.mpf:
    """Return the algebraic connectivity (Fiedler value) as a purely structural diagnostic."""
    for val in eigenvalues:
        if val > mp.mpf('1e-14'):
            return val
    return mp.mpf('0')

def random_walk_return_probabilities(state: RelationalState, max_steps: int) -> List[mp.mpf]:
    """Compute the return probability trace for random walks."""
    n = state.distinction_count()
    if n == 0:
        return []
    A = _get_adjacency_matrix(state)
    D = _get_degree_matrix(state, A)
    
    # Construct transition matrix P = D^-1 A
    P = matrix(n, n)
    for i in range(n):
        deg = D[i, i]
        if deg > 0:
            for j in range(n):
                P[i, j] = A[i, j] / deg

    probs = []
    # P_t is P^t
    P_t = matrix(n, n)
    for i in range(n):
        P_t[i, i] = 1.0

    for step in range(1, max_steps + 1):
        P_t = P_t * P
        trace = sum(P_t[i, i] for i in range(n))
        probs.append(trace / n)
    return probs

def log_slope_diagnostic(return_probs: List[mp.mpf], window_start: int, window_end: int) -> mp.mpf:
    """Compute the log-log slope of the return probability trace."""
    if window_end >= len(return_probs):
        window_end = len(return_probs) - 1
    if window_start >= window_end or window_start < 0:
        return mp.mpf('0')
    
    # slope = (log(y2) - log(y1)) / (log(x2) - log(x1))
    x1 = mp.mpf(window_start + 1)
    x2 = mp.mpf(window_end + 1)
    y1 = return_probs[window_start]
    y2 = return_probs[window_end]
    
    if y1 <= 0 or y2 <= 0:
        return mp.mpf('0')
        
    return (log(y2) - log(y1)) / (log(x2) - log(x1))

"""Observer stability tests for PR-2 diagnostics.

Status: [D] purely for software verification.
"""

from mpmath import mp
import random
from typing import List
from verification.pregeometry.primitives import RelationalState, state_from_edges
from verification.pregeometry.spectral_diagnostics import combinatorial_laplacian_spectrum

mp.dps = 80

def _permute_state(state: RelationalState, seed: int) -> RelationalState:
    """Relabel nodes using a random permutation to verify ordering invariance."""
    n = state.distinction_count()
    if n == 0:
        return state
        
    rng = random.Random(seed)
    labels = list(range(n))
    rng.shuffle(labels)
    
    edges = []
    for rel in state.relations:
        u = labels[rel.source.value]
        v = labels[rel.target.value]
        edges.append((u, v) if rel.directed else tuple(sorted((u, v))))
        
    # RelationalState expects deduplicated undirected edges
    if not any(rel.directed for rel in state.relations):
        edges = list(set(edges))
        
    return state_from_edges(n, edges, directed=False)

def verify_relabeling_invariance(state: RelationalState, seed: int = 42) -> bool:
    """Verify that spectral graph diagnostics are invariant under node relabeling."""
    base_spectrum = combinatorial_laplacian_spectrum(state)
    permuted_state = _permute_state(state, seed)
    permuted_spectrum = combinatorial_laplacian_spectrum(permuted_state)
    
    if len(base_spectrum) != len(permuted_spectrum):
        return False
        
    # Check residuals are below 1e-14
    for b, p in zip(base_spectrum, permuted_spectrum):
        if abs(b - p) > mp.mpf('1e-14'):
            return False
            
    return True

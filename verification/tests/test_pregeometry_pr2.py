"""Tests for PR-2 spectral graph diagnostics.

Status: [A] for software invariant checks.
"""

from mpmath import mp
import pytest
from verification.pregeometry.null_ensembles import pr0_state_trace
from verification.pregeometry.spectral_diagnostics import (
    combinatorial_laplacian_spectrum,
    compute_spectral_gap,
    random_walk_return_probabilities
)
from verification.pregeometry.observer_stability import verify_relabeling_invariance

# Rule 1: Precision initialization strictly locally declared
mp.dps = 80

def test_spectral_diagnostics_deterministic():
    """Ensure spectral properties are fully deterministic for PR-0 trace."""
    state = pr0_state_trace(15)[-1]
    
    spectrum_1 = combinatorial_laplacian_spectrum(state)
    spectrum_2 = combinatorial_laplacian_spectrum(state)
    
    # Must be exactly identical
    assert len(spectrum_1) == len(spectrum_2)
    for v1, v2 in zip(spectrum_1, spectrum_2):
        assert v1 == v2
        
    gap = compute_spectral_gap(spectrum_1)
    assert gap >= 0

def test_random_walk_probs_deterministic():
    """Ensure random walk return probabilities are fully deterministic."""
    state = pr0_state_trace(15)[-1]
    
    rw_1 = random_walk_return_probabilities(state, 5)
    rw_2 = random_walk_return_probabilities(state, 5)
    
    assert len(rw_1) == len(rw_2) == 5
    for v1, v2 in zip(rw_1, rw_2):
        assert v1 == v2

def test_observer_relabeling_invariance():
    """Ensure spectral gap and spectrum are invariant under node relabeling."""
    state = pr0_state_trace(20)[-1]
    is_invariant = verify_relabeling_invariance(state, seed=42)
    assert is_invariant is True

def test_no_forbidden_terms_in_api():
    """Ensure the API of spectral diagnostics does not leak physical target terms."""
    from verification.pregeometry import spectral_diagnostics
    
    source = open(spectral_diagnostics.__file__).read()
    forbidden = ["16.339", "dimension", "mass gap", "metric"]
    
    for f in forbidden:
        assert f not in source.lower(), f"Forbidden physical term '{f}' found in spectral_diagnostics.py"

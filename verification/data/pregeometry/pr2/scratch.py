from mpmath import mp
from verification.pregeometry.null_ensembles import pr0_state_trace
from verification.pregeometry.spectral_diagnostics import combinatorial_laplacian_spectrum
from verification.pregeometry.observer_stability import _permute_state

mp.dps = 80
state = pr0_state_trace(20)[-1]
base_spectrum = combinatorial_laplacian_spectrum(state)
permuted_state = _permute_state(state, 42)
permuted_spectrum = combinatorial_laplacian_spectrum(permuted_state)

print(f"Base len: {len(base_spectrum)}, Permuted len: {len(permuted_spectrum)}")
for b, p in zip(base_spectrum, permuted_spectrum):
    diff = abs(b - p)
    print(f"b: {b}, p: {p}, diff: {diff}")
    if diff > mp.mpf('1e-14'):
        print("FAILED HERE")

import numpy as np

rng = np.random.default_rng(42)
N = 15
alpha = 4.0
delta = 0.10
delta_min = alpha**2 * 0.75

H = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
H = (H + H.conj().T) / np.sqrt(2 * N)

evals = np.linalg.eigvalsh(H)
op_norm = max(abs(evals.min()), abs(evals.max()))
H_norm = H / op_norm

noise = (delta * delta_min) * H_norm
evals2 = np.linalg.eigvalsh(noise)
print(f"Noise operator norm: {max(abs(evals2.min()), abs(evals2.max()))}")
print(f"delta * delta_min: {delta * delta_min}")

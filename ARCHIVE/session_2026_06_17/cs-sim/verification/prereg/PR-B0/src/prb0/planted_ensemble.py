import numpy as np

def su2_generator(n: int, a: int) -> np.ndarray:
    """Returns the a-th generator of SU(2) in the spin-(n-1)/2 representation."""
    j = (n - 1) / 2.0
    m = np.arange(j, -j - 1e-9, -1)
    
    if a == 3:
        return np.diag(m)
    elif a == 1:
        off_diag = 0.5 * np.sqrt(j * (j + 1) - m[:-1] * m[1:])
        return np.diag(off_diag, k=1) + np.diag(off_diag, k=-1)
    elif a == 2:
        off_diag = -0.5j * np.sqrt(j * (j + 1) - m[:-1] * m[1:])
        return np.diag(off_diag, k=1) - np.diag(off_diag, k=-1)
    raise ValueError("a must be 1, 2, or 3")

def generate_planted_ensemble(partition: tuple, N: int, alpha: float, delta: float, rng: np.random.Generator) -> tuple:
    """
    X_a = α · ( ⊕_i L_a^{(n_i)} ) ⊕ 0_z ,   z = N − Σ nᵢ ,   a = 1,2,3
    X_a → X_a + (δ · Δ_min) · H_a ,  H_a Hermitian, ‖H_a‖_op = 1 (Wigner, normalized).
    Δ_min = α² · ¾
    """
    total_n = sum(partition)
    if total_n > N:
        raise ValueError("Sum of partition exceeds N")
    
    z = N - total_n
    
    matrices = []
    for a in (1, 2, 3):
        blocks = []
        for n_i in partition:
            blocks.append(alpha * su2_generator(n_i, a))
        if z > 0:
            blocks.append(np.zeros((z, z), dtype=np.complex128))
            
        from scipy.linalg import block_diag
        X_a = block_diag(*blocks) if blocks else np.zeros((N, N), dtype=np.complex128)
        
        # Noise
        if delta > 0:
            delta_min = alpha * np.sqrt(0.75)
            
            # Wigner matrix
            H = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
            H = (H + H.conj().T) / np.sqrt(2 * N)
            
            evals = np.linalg.eigvalsh(H)
            op_norm = max(abs(evals.min()), abs(evals.max()))
            if op_norm > 0:
                H_norm = H / op_norm
            else:
                H_norm = H
                
            X_a = X_a + (delta * delta_min) * H_norm
            
        matrices.append(X_a)
        
    return matrices[0], matrices[1], matrices[2]

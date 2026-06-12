"""
Hybrid Monte Carlo (HMC) with Leapfrog Integrator
===================================================
Implements the HMC sampler for Hermitian matrix models as specified in § 3.1.

Leapfrog integration:
    - Trajectory length τ = 1.0 (fixed, frozen)
    - Step size ε is auto-tuned during thermalization ONLY
    - Number of leapfrog steps L = round(τ / ε)

Acceptance criterion:
    - Standard Metropolis accept/reject on exp(-ΔH)
    - Auto-tuning adjusts ε to keep acceptance rate in [0.65, 0.85]

Phase-space variables:
    - Position:  X_a  (Hermitian N × N, a = 1,2,3)
    - Momentum:  P_a  (Hermitian N × N, drawn from Gaussian)

Hamiltonian:
    H = 1/2 * Σ_a Tr(P_a²)  +  S(X)

All arithmetic is IEEE-754 float64 (complex128 for matrices).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

from ..config import (
    HMC_ACCEPTANCE_HIGH,
    HMC_ACCEPTANCE_LOW,
    HMC_INITIAL_STEP_SIZE,
    HMC_TRAJECTORY_LENGTH,
)
from .action import Matrices, compute_action, compute_force

logger = logging.getLogger(__name__)


@dataclass
class HMCState:
    """Mutable state container for the HMC sampler."""

    X: Matrices                      # current position (X1, X2, X3)
    N: int                           # matrix size
    alpha: float                     # CS coupling
    mu2: float = 0.0                # mass deformation (M1)
    g2: float = 0.0                 # double-trace coupling (M1)
    step_size: float = HMC_INITIAL_STEP_SIZE
    trajectory_length: float = HMC_TRAJECTORY_LENGTH

    # Running statistics
    accepted: int = 0
    proposed: int = 0

    # Tuning control
    tuning_enabled: bool = True
    tuning_window: int = 50         # retune every 50 trajectories
    _window_accepted: int = field(default=0, repr=False)
    _window_proposed: int = field(default=0, repr=False)

    @property
    def acceptance_rate(self) -> float:
        """Global acceptance rate."""
        if self.proposed == 0:
            return 0.0
        return self.accepted / self.proposed

    @property
    def n_leapfrog_steps(self) -> int:
        """Number of leapfrog steps per trajectory."""
        return max(1, round(self.trajectory_length / self.step_size))


def _sample_momenta(N: int, rng: np.random.Generator) -> Matrices:
    """Draw conjugate momenta from the Gaussian distribution.

    Each P_a is a traceless Hermitian N × N matrix with entries drawn
    from the appropriate Gaussian ensemble:
        - Diagonal: N(0, 1) real
        - Upper off-diagonal: (N(0,1) + i*N(0,1)) / sqrt(2)
        - Lower off-diagonal: conjugate of upper
        - Then project to traceless
    """
    momenta = []
    for _ in range(3):
        # Real part
        re = rng.standard_normal((N, N))
        im = rng.standard_normal((N, N))
        P = (re + 1j * im) / np.sqrt(2.0)
        # Make Hermitian
        P = (P + P.conj().T) / 2.0
        # Make traceless
        P -= (np.trace(P) / N) * np.eye(N, dtype=np.complex128)
        momenta.append(P)
    return (momenta[0], momenta[1], momenta[2])


def _kinetic_energy(P: Matrices) -> float:
    """Compute K = 1/2 * Σ_a Tr(P_a²)."""
    return 0.5 * sum(np.trace(P[a] @ P[a]).real for a in range(3))


def _project_hermitian_traceless(M: np.ndarray, N: int) -> np.ndarray:
    """Project a matrix onto the traceless Hermitian subspace."""
    H = (M + M.conj().T) / 2.0
    H -= (np.trace(H) / N) * np.eye(N, dtype=np.complex128)
    return H


def _leapfrog(
    X: Matrices,
    P: Matrices,
    state: HMCState,
) -> tuple[Matrices, Matrices]:
    """Perform one full leapfrog integration trajectory.

    Standard leapfrog (Störmer-Verlet):
        P(ε/2) = P(0)  + (ε/2) * F(X(0))
        for step in 1..L-1:
            X(step*ε) = X((step-1)*ε)  + ε * P((step-1/2)*ε)
            P((step+1/2)*ε) = P((step-1/2)*ε) + ε * F(X(step*ε))
        X(L*ε) = X((L-1)*ε)  + ε * P((L-1/2)*ε)
        P(L*ε) = P((L-1/2)*ε) + (ε/2) * F(X(L*ε))

    Returns
    -------
    (X_new, P_new) : the updated position and momentum matrices.
    """
    eps = state.step_size
    N = state.N
    L = state.n_leapfrog_steps

    # Copy matrices
    X_cur = [X[a].copy() for a in range(3)]
    P_cur = [P[a].copy() for a in range(3)]

    X_tup = (X_cur[0], X_cur[1], X_cur[2])

    # Initial half-step for momenta
    F = compute_force(X_tup, N, state.alpha, state.mu2, state.g2)
    for a in range(3):
        P_cur[a] += (eps / 2.0) * F[a]
        P_cur[a] = _project_hermitian_traceless(P_cur[a], N)

    # Full steps
    for step in range(L - 1):
        # Full position step
        for a in range(3):
            X_cur[a] += eps * P_cur[a]
            X_cur[a] = _project_hermitian_traceless(X_cur[a], N)

        X_tup = (X_cur[0], X_cur[1], X_cur[2])

        # Full momentum step
        F = compute_force(X_tup, N, state.alpha, state.mu2, state.g2)
        for a in range(3):
            P_cur[a] += eps * F[a]
            P_cur[a] = _project_hermitian_traceless(P_cur[a], N)

    # Final full position step
    for a in range(3):
        X_cur[a] += eps * P_cur[a]
        X_cur[a] = _project_hermitian_traceless(X_cur[a], N)

    X_tup = (X_cur[0], X_cur[1], X_cur[2])

    # Final half-step for momenta
    F = compute_force(X_tup, N, state.alpha, state.mu2, state.g2)
    for a in range(3):
        P_cur[a] += (eps / 2.0) * F[a]
        P_cur[a] = _project_hermitian_traceless(P_cur[a], N)

    return (X_cur[0], X_cur[1], X_cur[2]), (P_cur[0], P_cur[1], P_cur[2])


def _tune_step_size(state: HMCState) -> None:
    """Adjust the leapfrog step size to maintain acceptance rate in [0.65, 0.85].

    Called every `state.tuning_window` trajectories during thermalization.
    Uses a multiplicative update:
        - If rate < 0.65: shrink ε by factor 0.9
        - If rate > 0.85: grow ε by factor 1.1
        - Otherwise: no change

    Bounds: ε ∈ [1e-4, 1.0].
    """
    if state._window_proposed == 0:
        return

    rate = state._window_accepted / state._window_proposed

    if rate < 0.01:
        # Emergency: no accepts at all → halve step size
        state.step_size *= 0.5
    elif rate < HMC_ACCEPTANCE_LOW:
        state.step_size *= 0.8
    elif rate > HMC_ACCEPTANCE_HIGH:
        state.step_size *= 1.1

    # Clamp to sensible range
    state.step_size = max(1e-4, min(1.0, state.step_size))

    logger.debug(
        "HMC tune: window rate=%.3f, new ε=%.6f (L=%d)",
        rate, state.step_size, state.n_leapfrog_steps,
    )

    # Reset window counters
    state._window_accepted = 0
    state._window_proposed = 0


def hmc_step(state: HMCState, rng: np.random.Generator) -> float:
    """Perform one HMC trajectory (propose + accept/reject).

    Parameters
    ----------
    state : HMCState
        Mutable sampler state.  Updated in-place on acceptance.
    rng : np.random.Generator
        Random number generator for momentum sampling and accept/reject.

    Returns
    -------
    float
        The action value S(X) after this step (whether accepted or rejected).
    """
    N = state.N
    X_old = state.X

    # Draw momenta
    P_old = _sample_momenta(N, rng)

    # Current Hamiltonian
    S_old = compute_action(X_old, N, state.alpha, state.mu2, state.g2).total
    K_old = _kinetic_energy(P_old)
    H_old = S_old + K_old

    # Leapfrog integration
    X_new, P_new = _leapfrog(X_old, P_old, state)

    # New Hamiltonian
    S_new = compute_action(X_new, N, state.alpha, state.mu2, state.g2).total
    K_new = _kinetic_energy(P_new)
    H_new = S_new + K_new

    # Metropolis accept/reject
    delta_H = H_new - H_old
    state.proposed += 1
    state._window_proposed += 1

    # NaN/Inf guard: if leapfrog diverged, ALWAYS reject
    if not np.isfinite(delta_H):
        # Reject: keep old configuration (leapfrog overflow)
        action_val = S_old
        logger.debug("HMC reject: delta_H=%s (non-finite), keeping old config.", delta_H)
    elif delta_H < 0.0 or rng.random() < np.exp(-delta_H):
        # Accept
        state.X = X_new
        state.accepted += 1
        state._window_accepted += 1
        action_val = S_new
    else:
        # Reject: keep old configuration
        action_val = S_old

    # Step-size tuning (only during thermalization)
    if state.tuning_enabled and state._window_proposed >= state.tuning_window:
        _tune_step_size(state)

    return action_val

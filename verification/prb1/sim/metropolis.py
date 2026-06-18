"""
Metropolis Variation Arm
=========================
Implements a single-matrix Metropolis-Hastings update for comparison with HMC.

This sampler is a secondary arm: it updates one matrix element at a time
(entry-wise random walk on the space of traceless Hermitian matrices).

Adaptive proposal width:
    - During thermalization, the proposal width σ is tuned to maintain
      an acceptance rate of ~50 ± 15%.
    - After thermalization, σ is frozen.

This module is called as an alternative to HMC and produces the same
observable interface (raw spectrum arrays, no scoring).

IEEE-754 float64 throughout.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

from ..config import (
    HMC_TRAJECTORY_LENGTH,
)
from .action import Matrices, compute_action

logger = logging.getLogger(__name__)

# Metropolis acceptance-rate bounds (distinct from HMC)
METROPOLIS_ACCEPTANCE_LOW: float = 0.35
METROPOLIS_ACCEPTANCE_HIGH: float = 0.65
METROPOLIS_INITIAL_WIDTH: float = 0.5


@dataclass
class MetropolisState:
    """Mutable state container for the Metropolis sampler."""

    X: Matrices                         # current position (X1, X2, X3)
    N: int                              # matrix size
    alpha: float                        # CS coupling
    mu2: float = 0.0                   # mass deformation (M1)
    g2: float = 0.0                    # double-trace coupling (M1)
    proposal_width: float = METROPOLIS_INITIAL_WIDTH

    # Running statistics
    accepted: int = 0
    proposed: int = 0

    # Tuning control
    tuning_enabled: bool = True
    tuning_window: int = 200
    _window_accepted: int = field(default=0, repr=False)
    _window_proposed: int = field(default=0, repr=False)

    @property
    def acceptance_rate(self) -> float:
        """Global acceptance rate."""
        if self.proposed == 0:
            return 0.0
        return self.accepted / self.proposed


def _propose_hermitian_perturbation(
    X_a: np.ndarray,
    N: int,
    sigma: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Propose a small random traceless Hermitian perturbation to X_a.

    Selects a random entry (i, j) and perturbs:
        - If i == j: add N(0, sigma) to the real diagonal, then remove trace.
        - If i != j: add N(0, sigma/sqrt(2)) to both real and imaginary parts
          of (i,j), and the conjugate to (j,i).

    Returns
    -------
    np.ndarray
        The proposed new matrix X_a' (N × N complex128 Hermitian).
    """
    X_new = X_a.copy()

    # Pick random entry
    i = rng.integers(0, N)
    j = rng.integers(0, N)

    if i == j:
        # Diagonal perturbation (real)
        delta = rng.standard_normal() * sigma
        X_new[i, i] += delta
        # Remove trace to maintain tracelessness
        X_new -= (np.trace(X_new) / N) * np.eye(N, dtype=np.complex128)
    elif i < j:
        # Off-diagonal perturbation (complex)
        delta_re = rng.standard_normal() * sigma / np.sqrt(2.0)
        delta_im = rng.standard_normal() * sigma / np.sqrt(2.0)
        delta = delta_re + 1j * delta_im
        X_new[i, j] += delta
        X_new[j, i] += delta.conj()
    else:
        # i > j: perturb (j, i) and its conjugate
        delta_re = rng.standard_normal() * sigma / np.sqrt(2.0)
        delta_im = rng.standard_normal() * sigma / np.sqrt(2.0)
        delta = delta_re + 1j * delta_im
        X_new[j, i] += delta
        X_new[i, j] += delta.conj()

    return X_new


def _tune_proposal_width(state: MetropolisState) -> None:
    """Adjust the proposal width to maintain acceptance rate in [0.35, 0.65].

    Uses multiplicative update:
        - If rate < 0.35: shrink σ by 0.9
        - If rate > 0.65: grow σ by 1.1
    Bounds: σ ∈ [1e-5, 10.0].
    """
    if state._window_proposed == 0:
        return

    rate = state._window_accepted / state._window_proposed

    if rate < METROPOLIS_ACCEPTANCE_LOW:
        state.proposal_width *= 0.9
    elif rate > METROPOLIS_ACCEPTANCE_HIGH:
        state.proposal_width *= 1.1

    state.proposal_width = max(1e-5, min(10.0, state.proposal_width))

    logger.debug(
        "Metropolis tune: window rate=%.3f, new σ=%.6f",
        rate, state.proposal_width,
    )

    state._window_accepted = 0
    state._window_proposed = 0


def metropolis_sweep(state: MetropolisState, rng: np.random.Generator) -> float:
    """Perform one full Metropolis sweep (3 × N² entry proposals).

    A "sweep" proposes N² perturbations per matrix (3 matrices), mirroring
    one HMC trajectory in terms of computational effort per "trajectory".

    Parameters
    ----------
    state : MetropolisState
        Mutable sampler state, updated in-place.
    rng : np.random.Generator
        Random number generator.

    Returns
    -------
    float
        The action value S(X) after the full sweep.
    """
    N = state.N
    n_proposals_per_sweep = 3 * N * N
    S_current = compute_action(
        state.X, N, state.alpha, state.mu2, state.g2
    ).total

    X_list = [state.X[0].copy(), state.X[1].copy(), state.X[2].copy()]

    for _ in range(n_proposals_per_sweep):
        # Pick which matrix to perturb
        a = rng.integers(0, 3)

        # Propose
        X_proposed = _propose_hermitian_perturbation(
            X_list[a], N, state.proposal_width, rng
        )

        # Build the proposed triple
        X_trial = list(X_list)
        X_trial[a] = X_proposed
        X_trial_tup = (X_trial[0], X_trial[1], X_trial[2])

        # Compute new action
        S_proposed = compute_action(
            X_trial_tup, N, state.alpha, state.mu2, state.g2
        ).total

        # Metropolis accept/reject
        delta_S = S_proposed - S_current
        state.proposed += 1
        state._window_proposed += 1

        if delta_S < 0.0 or rng.random() < np.exp(-delta_S):
            X_list[a] = X_proposed
            S_current = S_proposed
            state.accepted += 1
            state._window_accepted += 1

    # Update state
    state.X = (X_list[0], X_list[1], X_list[2])

    # Tune proposal width during thermalization
    if state.tuning_enabled and state._window_proposed >= state.tuning_window:
        _tune_proposal_width(state)

    return S_current

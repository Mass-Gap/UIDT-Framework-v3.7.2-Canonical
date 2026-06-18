"""
Thermalization Detection and Effective Sample Size
====================================================
Implements § 3.2 of the preregistration protocol.

Thermalization criterion (running-mean convergence):
    1. Partition the action-density time series S/N² into contiguous
       windows of THERMALIZATION_WINDOW = 200 trajectories.
    2. For each consecutive window pair (w_{k-1}, w_k), compute the
       change in window means: δ = |mean(w_k) - mean(w_{k-1})|.
    3. Compute the standard error of the later window:
       SE = std(w_k) / sqrt(|w_k|).
    4. Thermalization is declared when δ < THERMALIZATION_TOLERANCE_SE × SE
       AND at least THERMALIZATION_MIN_TRAJECTORIES have elapsed.

Effective Sample Size (ESS):
    Estimated via the initial monotone sequence estimator (IMSE) of the
    integrated autocorrelation time τ_int:
        ESS = n / (2 * τ_int)
    where n is the number of production measurements.

IEEE-754 float64 throughout.
"""

from __future__ import annotations

import logging

import numpy as np

from ..config import (
    MIN_EFFECTIVE_SAMPLE_SIZE,
    THERMALIZATION_MIN_TRAJECTORIES,
    THERMALIZATION_TOLERANCE_SE,
    THERMALIZATION_WINDOW,
)

logger = logging.getLogger(__name__)


def detect_thermalization(action_density_series: np.ndarray) -> int:
    """Determine the thermalization cutoff index.

    Parameters
    ----------
    action_density_series : np.ndarray
        1-D array of S/N² values, one per trajectory.

    Returns
    -------
    int
        Index of the first post-thermalization trajectory.
        If thermalization is never achieved, returns len(series).
    """
    n = len(action_density_series)
    W = THERMALIZATION_WINDOW

    if n < THERMALIZATION_MIN_TRAJECTORIES:
        # Cannot declare thermalization before minimum
        return n

    # Slide through consecutive window pairs
    n_windows = n // W
    if n_windows < 2:
        return n

    for k in range(1, n_windows):
        traj_index = (k + 1) * W
        if traj_index < THERMALIZATION_MIN_TRAJECTORIES:
            continue

        w_prev = action_density_series[(k - 1) * W : k * W]
        w_curr = action_density_series[k * W : (k + 1) * W]

        mean_prev = np.mean(w_prev)
        mean_curr = np.mean(w_curr)
        delta = abs(mean_curr - mean_prev)

        se_curr = np.std(w_curr, ddof=1) / np.sqrt(len(w_curr))

        if se_curr > 0.0 and delta < THERMALIZATION_TOLERANCE_SE * se_curr:
            logger.info(
                "Thermalization detected at trajectory %d "
                "(δ=%.6e, %.1f × SE=%.6e)",
                traj_index, delta, THERMALIZATION_TOLERANCE_SE, se_curr,
            )
            return traj_index

    logger.warning(
        "Thermalization NOT detected after %d trajectories", n,
    )
    return n


def _autocorrelation_function(x: np.ndarray, max_lag: int | None = None) -> np.ndarray:
    """Compute the normalised autocorrelation function C(t) of a 1-D signal.

    C(t) = <(x_i - <x>)(x_{i+t} - <x>)> / Var(x)

    Uses FFT for efficiency.

    Parameters
    ----------
    x : np.ndarray
        1-D time series.
    max_lag : int or None
        Maximum lag to compute.  Default: len(x) // 2.

    Returns
    -------
    np.ndarray
        Normalised autocorrelation for lags 0..max_lag-1.
    """
    n = len(x)
    if max_lag is None:
        max_lag = n // 2

    x_centered = x - np.mean(x)
    variance = np.var(x, ddof=0)
    if variance == 0.0:
        return np.ones(max_lag)

    # FFT-based autocorrelation
    fft_len = 2 * n  # zero-padded for linear (not circular) correlation
    x_fft = np.fft.rfft(x_centered, n=fft_len)
    power = np.abs(x_fft) ** 2
    acf_full = np.fft.irfft(power, n=fft_len)[:n]
    acf_full /= acf_full[0]  # normalise so C(0) = 1

    return acf_full[:max_lag]


def integrated_autocorrelation_time(x: np.ndarray) -> float:
    """Estimate the integrated autocorrelation time τ_int using IMSE.

    The initial monotone sequence estimator (Geyer, 1992):
        τ_int = -1/2 + Σ_{t=0}^{M} C(t)
    where M is determined by the first time the sum of consecutive pairs
    C(2k) + C(2k+1) becomes negative.

    Parameters
    ----------
    x : np.ndarray
        1-D time series of measurements.

    Returns
    -------
    float
        Estimated τ_int.  Always ≥ 0.5.
    """
    n = len(x)
    if n < 4:
        return float(n)

    max_lag = n // 2
    acf = _autocorrelation_function(x, max_lag)

    # IMSE: sum consecutive pairs until pair sum becomes negative
    tau = -0.5 + acf[0]  # C(0) = 1.0

    k = 1
    while 2 * k + 1 < max_lag:
        pair_sum = acf[2 * k] + acf[2 * k + 1]
        if pair_sum <= 0.0:
            break
        tau += pair_sum
        k += 1

    return max(0.5, tau)


def effective_sample_size(measurements: np.ndarray) -> float:
    """Compute the effective sample size (ESS) of a measurement time series.

    ESS = n / (2 * τ_int)

    Parameters
    ----------
    measurements : np.ndarray
        1-D array of production-phase measurements (e.g., action density).

    Returns
    -------
    float
        Estimated ESS.
    """
    n = len(measurements)
    if n < 4:
        return float(n)

    tau_int = integrated_autocorrelation_time(measurements)
    ess = n / (2.0 * tau_int)

    if ess < MIN_EFFECTIVE_SAMPLE_SIZE:
        logger.warning(
            "ESS=%.1f < %d (UNDERSAMPLED). τ_int=%.2f, n=%d",
            ess, MIN_EFFECTIVE_SAMPLE_SIZE, tau_int, n,
        )

    return ess


def is_undersampled(ess: float) -> bool:
    """Check if the effective sample size indicates undersampling."""
    return ess < MIN_EFFECTIVE_SAMPLE_SIZE

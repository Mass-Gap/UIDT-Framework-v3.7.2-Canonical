"""
Cell-Level Runner — Orchestrates Single-Cell Simulation
=========================================================
Implements the full simulation pipeline for one (cell, seed_index) run:

    1. Generate deterministic RNG and initial conditions.
    2. Thermalization phase (HMC with auto-tuned step size).
    3. Freeze step size; switch to production.
    4. Production phase: 8000 trajectories, measure every 10th.
    5. Compute ESS on action-density production time series.
    6. Save raw spectra, scalars, and metadata as .npz + JSON.

Output contains ZERO partition detection or scoring logic.
The runner emits unclassified raw data only.

IEEE-754 float64 throughout.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

import numpy as np

from ..config import (
    MEASUREMENT_INTERVAL,
    PRODUCTION_TRAJECTORIES,
    RAW_DATA_DIR,
    GridCell,
    build_grid,
    build_pilot_grid,
)
from .action import compute_action
from .hmc import HMCState, hmc_step
from .observables import extract_observables
from .seeds import is_cold, is_hot, make_initial_matrices, make_rng
from .thermalization import (
    detect_thermalization,
    effective_sample_size,
    is_undersampled,
)

logger = logging.getLogger(__name__)

# Maximum thermalization trajectories before giving up
MAX_THERMALIZATION_TRAJECTORIES: int = 20000


def _ensure_output_dir(output_dir: Path) -> None:
    """Create the output directory if it does not exist."""
    output_dir.mkdir(parents=True, exist_ok=True)


def run_single_cell(
    cell: GridCell,
    seed_index: int,
    output_dir: Path | None = None,
    sampler: str = "hmc",
) -> dict[str, Any]:
    """Execute the full simulation for one (cell, seed_index) pair.

    Parameters
    ----------
    cell : GridCell
        Parameter-grid point (model, N, alpha_tilde, mu2, g2).
    seed_index : int
        Seed index in [0, 8).
    output_dir : Path or None
        Where to write the .npz output.  Default: config.RAW_DATA_DIR.
    sampler : str
        Sampling algorithm: "hmc" (default) or "metropolis".

    Returns
    -------
    dict
        Metadata dictionary with run_uuid, timing, thermalization info, ESS.
    """
    if output_dir is None:
        output_dir = RAW_DATA_DIR
    _ensure_output_dir(output_dir)

    run_uuid = str(uuid.uuid4())
    t_start = time.time()

    N = cell.N
    alpha = cell.alpha_tilde
    mu2 = cell.mu2
    g2 = cell.g2

    logger.info(
        "Starting run %s: %s N=%d α̃=%.2f μ²=%.2f g2=%.2f seed=%d sampler=%s",
        run_uuid, cell.model, N, alpha, mu2, g2, seed_index, sampler,
    )

    # --- 1. Initialisation ---
    rng = make_rng(cell, seed_index)
    X = make_initial_matrices(cell, seed_index, rng)

    # --- 2. Thermalization phase ---
    if sampler == "hmc":
        therm_result = _thermalize_hmc(X, N, alpha, mu2, g2, rng)
    elif sampler == "metropolis":
        therm_result = _thermalize_metropolis(X, N, alpha, mu2, g2, rng)
    else:
        raise ValueError(f"Unknown sampler: {sampler!r}. Use 'hmc' or 'metropolis'.")

    X_thermalized = therm_result["X"]
    therm_traj = therm_result["n_thermalization_trajectories"]
    therm_action_series = therm_result["action_density_series"]
    step_size_final = therm_result.get("step_size_final", None)
    proposal_width_final = therm_result.get("proposal_width_final", None)
    therm_acceptance_rate = therm_result["acceptance_rate"]

    logger.info(
        "Thermalization complete: %d trajectories, acceptance=%.3f",
        therm_traj, therm_acceptance_rate,
    )

    # --- 3. Production phase ---
    prod_result = _production_phase(
        X_thermalized, N, alpha, mu2, g2, rng, sampler,
        step_size=step_size_final,
        proposal_width=proposal_width_final,
    )

    # --- 4. Compute ESS ---
    action_densities_prod = prod_result["action_density_measurements"]
    ess = effective_sample_size(action_densities_prod)

    t_end = time.time()
    wall_time_s = t_end - t_start

    # --- 5. Assemble metadata ---
    metadata: dict[str, Any] = {
        "run_uuid": run_uuid,
        "model": cell.model,
        "N": N,
        "alpha_tilde": alpha,
        "mu2": mu2,
        "g2": g2,
        "seed_index": seed_index,
        "start_type": "hot" if is_hot(seed_index) else "cold",
        "sampler": sampler,
        "n_thermalization_trajectories": therm_traj,
        "thermalization_acceptance_rate": float(therm_acceptance_rate),
        "production_trajectories": PRODUCTION_TRAJECTORIES,
        "measurement_interval": MEASUREMENT_INTERVAL,
        "n_measurements": prod_result["n_measurements"],
        "ess_action_density": float(ess),
        "undersampled": is_undersampled(ess),
        "wall_time_seconds": wall_time_s,
        "production_acceptance_rate": float(prod_result["acceptance_rate"]),
    }
    if step_size_final is not None:
        metadata["hmc_step_size_final"] = float(step_size_final)
    if proposal_width_final is not None:
        metadata["metropolis_proposal_width_final"] = float(proposal_width_final)

    # --- 6. Save output ---
    npz_filename = f"{run_uuid}.npz"
    npz_path = output_dir / npz_filename
    json_path = output_dir / f"{run_uuid}.json"

    np.savez_compressed(
        str(npz_path),
        casimir_spectra=prod_result["casimir_spectra"],
        x3_spectra=prod_result["x3_spectra"],
        action_density=action_densities_prod,
        casimir_trace_per_N=prod_result["casimir_trace_per_N_measurements"],
        myers_values=prod_result["myers_measurements"],
        thermalization_action_density=np.asarray(therm_action_series, dtype=np.float64),
    )

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    logger.info(
        "Run %s complete: %.1f s, ESS=%.1f, saved to %s",
        run_uuid, wall_time_s, ess, npz_path,
    )

    return metadata


# =========================================================================
# Internal: Thermalization
# =========================================================================

def _thermalize_hmc(
    X, N, alpha, mu2, g2, rng,
) -> dict[str, Any]:
    """Run HMC thermalization with step-size tuning."""
    from .hmc import HMCState, hmc_step

    state = HMCState(
        X=X, N=N, alpha=alpha, mu2=mu2, g2=g2,
        tuning_enabled=True,
    )

    action_series: list[float] = []
    traj = 0

    while traj < MAX_THERMALIZATION_TRAJECTORIES:
        action_val = hmc_step(state, rng)
        action_density = action_val / (N * N)
        action_series.append(action_density)
        traj += 1

        # Check thermalization every WINDOW trajectories after MIN
        if traj >= 2000 and traj % 200 == 0:
            cutoff = detect_thermalization(np.asarray(action_series))
            if cutoff < traj:
                break

    # Freeze step size
    state.tuning_enabled = False

    return {
        "X": state.X,
        "n_thermalization_trajectories": traj,
        "action_density_series": action_series,
        "step_size_final": state.step_size,
        "acceptance_rate": state.acceptance_rate,
    }


def _thermalize_metropolis(
    X, N, alpha, mu2, g2, rng,
) -> dict[str, Any]:
    """Run Metropolis thermalization with proposal-width tuning."""
    from .metropolis import MetropolisState, metropolis_sweep

    state = MetropolisState(
        X=X, N=N, alpha=alpha, mu2=mu2, g2=g2,
        tuning_enabled=True,
    )

    action_series: list[float] = []
    traj = 0

    while traj < MAX_THERMALIZATION_TRAJECTORIES:
        action_val = metropolis_sweep(state, rng)
        action_density = action_val / (N * N)
        action_series.append(action_density)
        traj += 1

        if traj >= 2000 and traj % 200 == 0:
            cutoff = detect_thermalization(np.asarray(action_series))
            if cutoff < traj:
                break

    state.tuning_enabled = False

    return {
        "X": state.X,
        "n_thermalization_trajectories": traj,
        "action_density_series": action_series,
        "proposal_width_final": state.proposal_width,
        "acceptance_rate": state.acceptance_rate,
    }


# =========================================================================
# Internal: Production
# =========================================================================

def _production_phase(
    X, N, alpha, mu2, g2, rng, sampler,
    step_size=None, proposal_width=None,
) -> dict[str, Any]:
    """Run the production phase: PRODUCTION_TRAJECTORIES with measurements."""

    n_measurements = PRODUCTION_TRAJECTORIES // MEASUREMENT_INTERVAL

    # Pre-allocate arrays
    casimir_spectra = np.zeros((n_measurements, N), dtype=np.float64)
    x3_spectra = np.zeros((n_measurements, N), dtype=np.float64)
    action_density_meas = np.zeros(n_measurements, dtype=np.float64)
    casimir_trace_meas = np.zeros(n_measurements, dtype=np.float64)
    myers_meas = np.zeros(n_measurements, dtype=np.float64)

    if sampler == "hmc":
        from .hmc import HMCState, hmc_step

        state = HMCState(
            X=X, N=N, alpha=alpha, mu2=mu2, g2=g2,
            step_size=step_size if step_size is not None else 0.1,
            tuning_enabled=False,
        )

        meas_idx = 0
        for traj in range(PRODUCTION_TRAJECTORIES):
            hmc_step(state, rng)

            if (traj + 1) % MEASUREMENT_INTERVAL == 0:
                obs = extract_observables(state.X, N, alpha, mu2, g2)
                casimir_spectra[meas_idx] = obs.casimir_eigenvalues
                x3_spectra[meas_idx] = obs.x3_eigenvalues
                action_density_meas[meas_idx] = obs.action_density
                casimir_trace_meas[meas_idx] = obs.casimir_trace_per_N
                myers_meas[meas_idx] = obs.myers_value
                meas_idx += 1

        acceptance_rate = state.acceptance_rate

    elif sampler == "metropolis":
        from .metropolis import MetropolisState, metropolis_sweep

        state = MetropolisState(
            X=X, N=N, alpha=alpha, mu2=mu2, g2=g2,
            proposal_width=proposal_width if proposal_width is not None else 0.5,
            tuning_enabled=False,
        )

        meas_idx = 0
        for traj in range(PRODUCTION_TRAJECTORIES):
            metropolis_sweep(state, rng)

            if (traj + 1) % MEASUREMENT_INTERVAL == 0:
                obs = extract_observables(state.X, N, alpha, mu2, g2)
                casimir_spectra[meas_idx] = obs.casimir_eigenvalues
                x3_spectra[meas_idx] = obs.x3_eigenvalues
                action_density_meas[meas_idx] = obs.action_density
                casimir_trace_meas[meas_idx] = obs.casimir_trace_per_N
                myers_meas[meas_idx] = obs.myers_value
                meas_idx += 1

        acceptance_rate = state.acceptance_rate
    else:
        raise ValueError(f"Unknown sampler: {sampler!r}")

    return {
        "casimir_spectra": casimir_spectra,
        "x3_spectra": x3_spectra,
        "action_density_measurements": action_density_meas,
        "casimir_trace_per_N_measurements": casimir_trace_meas,
        "myers_measurements": myers_meas,
        "n_measurements": n_measurements,
        "acceptance_rate": acceptance_rate,
    }


# =========================================================================
# Grid-level orchestration
# =========================================================================

def run_grid(
    cells: list[GridCell] | None = None,
    seeds: range | None = None,
    output_dir: Path | None = None,
    sampler: str = "hmc",
) -> list[dict[str, Any]]:
    """Run the full simulation across all grid cells in lexicographic order.

    Parameters
    ----------
    cells : list[GridCell] or None
        Parameter grid.  Default: build_grid() (full grid).
    seeds : range or None
        Seed indices to run.  Default: range(8).
    output_dir : Path or None
        Output directory.  Default: config.RAW_DATA_DIR.
    sampler : str
        Sampling algorithm: "hmc" or "metropolis".

    Returns
    -------
    list[dict]
        List of metadata dictionaries, one per run.
    """
    if cells is None:
        cells = build_grid()
    if seeds is None:
        seeds = range(8)

    all_metadata: list[dict[str, Any]] = []

    total_runs = len(cells) * len(seeds)
    run_num = 0

    for cell in cells:
        for seed_idx in seeds:
            run_num += 1
            logger.info(
                "=== Run %d / %d ===", run_num, total_runs,
            )
            meta = run_single_cell(
                cell, seed_idx, output_dir=output_dir, sampler=sampler,
            )
            all_metadata.append(meta)

    return all_metadata


def run_pilot(
    output_dir: Path | None = None,
    sampler: str = "hmc",
) -> list[dict[str, Any]]:
    """Run the pilot grid (M0, N ∈ {16, 24, 32} only).

    The pilot is for thermalization testing and acceptance-rate validation.
    """
    cells = build_pilot_grid()
    return run_grid(cells=cells, output_dir=output_dir, sampler=sampler)

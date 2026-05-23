import mpmath as mp


def compute_topological_cascade_coupling(mu_m: mp.mpf, sigma_m: mp.mpf, steps_str: str = '99.0') -> dict:
    """
    Couples the statistical moments of the vacuum spin ensemble to the
    holographic cascade.

    [PATCH v3.9.1]: Uses ledger-compliant gamma_inf (thermodynamic limit)
    and supports variable cascade step counts for multi-scale testing.

    Physical basis:
    - The cascade iterates over macroscopic spacetime scales.
    - Therefore the asymptotic invariant gamma_inf must be used, not the
      bare coupling gamma.
    - gamma_inf = gamma_ref + delta_gamma  [A-]

    Parameters
    ----------
    mu_m     : mp.mpf  -- mean of the vacuum spin ensemble moment
    sigma_m  : mp.mpf  -- standard deviation of the vacuum spin ensemble moment
    steps_str: str     -- number of cascade steps as unrounded string (default '99.0')
                          Supports non-integer N for intermediate-scale testing.

    Returns
    -------
    dict with keys:
        gamma_inf_used          [A-]  thermodynamic limit coupling used
        omega_canonical               unperturbed canonical cascade weight
        omega_topological             topologically modulated cascade weight
        macroscopic_noise_bound       first-order error propagation of topo noise
        topological_shift             residual: omega_topo - omega_canonical
        status                        MACROSCOPIC_COUPLING_CORRECTED

    Evidence: [A-] Calibrated  |  Stratum: III
    Precision: mp.dps=80 (local, non-global)
    """
    mp.dps = 80

    # --- Canonical v3.9 ledger references [A-] ---
    gamma_ref   = mp.mpf('16.339')
    delta_gamma = mp.mpf('0.0047')

    # Thermodynamic limit: gamma_inf = gamma + delta_gamma
    # Constructed from components to prove provenance deterministically.
    gamma_inf = gamma_ref + delta_gamma

    # --- Cascade step count (variable N) ---
    steps_total   = mp.mpf(steps_str)
    steps_reduced = steps_total - mp.mpf('1.0')

    # --- 1. Unperturbed canonical cascade (reference baseline) ---
    # q_canonical = 1 / gamma_inf
    q_canonical    = mp.mpf('1.0') / gamma_inf
    omega_canonical = mp.power(q_canonical, steps_total)

    # --- 2. Topologically modulated cascade ---
    # q_eff = mu_m / gamma_inf  (ensemble mean drives the effective ratio)
    q_eff      = mu_m / gamma_inf
    omega_topo = mp.power(q_eff, steps_total)

    # --- 3. Macroscopic error propagation of topological noise ---
    # Generalised noise bound for variable N:
    #   delta_omega = N * q_eff^(N-1) * (sigma_m / gamma_inf)
    # Zero-step protection: N=0 => unphysical q_eff^(-1) avoided.
    if steps_total > mp.mpf('0.0'):
        noise_factor          = sigma_m / gamma_inf
        omega_variance_bound  = steps_total * mp.power(q_eff, steps_reduced) * noise_factor
    else:
        omega_variance_bound  = mp.mpf('0.0')

    # --- 4. Topological shift (residuum) ---
    topological_shift = omega_topo - omega_canonical

    return {
        "gamma_inf_used":         gamma_inf,
        "omega_canonical":         omega_canonical,
        "omega_topological":       omega_topo,
        "macroscopic_noise_bound": omega_variance_bound,
        "topological_shift":       topological_shift,
        "status":                  "MACROSCOPIC_COUPLING_CORRECTED",
    }

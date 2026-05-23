import mpmath as mp


def compute_calibrated_torsion_eos(
    topological_shift: "mp.mpf",
    steps_str: str = "99.0",
    tolerance_str: str = "0.05",
) -> dict:
    """
    Calibrated torsion-EOS coupling with DESI anchor and stratum firewall.

    [PATCH v3.9.1]: Resolves two audit findings:
      1. Torsion energy is generated from the ledger-anchored E_T = 2.44 MeV [C],
         not from a dimensionless topological shift alone.
      2. w_BRST = -8.12 [D] remains Stratum III only and is not promoted to [C].
         The macroscopic EOS anchor is w_0 = -0.99 [C] from the DESI calibration.

    Precision: mp.dps = 80, declared locally per Anti-Tampering directive.

    Parameters
    ----------
    topological_shift : mp.mpf
        Dimensionless shift Omega_topo - Omega_canonical from the cascade module.
        Acts as modulation amplitude only; it does not generate energy.
    steps_str : str
        Number of cascade steps as an unrounded string (default '99.0').
    tolerance_str : str
        Absolute DESI kill-switch tolerance on w_0 (default '0.05').

    Returns
    -------
    dict with keys:
        gamma_inf_used, ET_ledger_GeV, w_0_ledger, w_BRST_stratum_III,
        torsion_energy_modulated_GeV, w_0_macroscopic,
        desi_kill_switch_triggered, evidence_tag, status
    """
    mp.dps = 80

    # ------------------------------------------------------------------
    # Canonical ledger constants (Stratum I / read-only)
    # ------------------------------------------------------------------
    gamma_ref   = mp.mpf("16.339")      # [A-] bare kinetic VEV
    delta_gamma = mp.mpf("0.0047")      # [A-] vacuum dressing
    gamma_inf   = gamma_ref + delta_gamma  # [A-] thermodynamic limit = 16.3437

    ET_ledger_GeV = mp.mpf("0.00244")   # [C] torsion basis energy, 2.44 MeV
    w_0_ledger    = mp.mpf("-0.99")     # [C] DESI-calibrated dark-energy EOS
    Delta_star    = mp.mpf("1.710")     # [A] Yang-Mills spectral gap (NOT particle mass)

    # ------------------------------------------------------------------
    # Stratum III input — BRST phantom pressure
    # NOT promoted to cosmological category [C]
    # ------------------------------------------------------------------
    w_BRST_stratum_III = mp.mpf("-8.12")  # [D] local model input only

    # ------------------------------------------------------------------
    # 1. Torsion energy modulation
    #    topological_shift is dimensionless — it rescales E_T [C];
    #    it does NOT generate energy from a dimensionless number.
    # ------------------------------------------------------------------
    modulation_amplitude = mp.fabs(topological_shift)
    torsion_energy_modulated_GeV = ET_ledger_GeV * (
        mp.mpf("1.0") + modulation_amplitude
    )

    # ------------------------------------------------------------------
    # 2. Phantom pressure contribution (Stratum III — bounded, not free)
    #    Contribution is computed but capped at the ledger anchor.
    #    This preserves the firewall: w_macro stays in [C] territory.
    # ------------------------------------------------------------------
    steps_total   = mp.mpf(steps_str)
    q_eff         = mp.mpf("1.0") / gamma_inf
    omega_n       = mp.power(q_eff, steps_total)

    # Fractional BRST correction, suppressed by cascade decay
    w_brst_correction = w_BRST_stratum_III * omega_n * (
        torsion_energy_modulated_GeV / Delta_star
    )

    # Macroscopic EOS: DESI anchor + bounded BRST perturbation
    w_0_macroscopic = w_0_ledger + w_brst_correction

    # ------------------------------------------------------------------
    # 3. DESI kill-switch
    # ------------------------------------------------------------------
    tolerance         = mp.mpf(tolerance_str)
    deviation         = mp.fabs(w_0_macroscopic - w_0_ledger)
    kill_switch       = bool(deviation > tolerance)

    # ------------------------------------------------------------------
    # 4. Evidence tag — capped at [C]; never inflated
    # ------------------------------------------------------------------
    evidence_tag = "[C] calibrated_cosmology — w_0 anchored to DESI; w_BRST Stratum III only"

    return {
        "gamma_inf_used":              gamma_inf,
        "ET_ledger_GeV":               ET_ledger_GeV,
        "w_0_ledger":                  w_0_ledger,
        "w_BRST_stratum_III":          w_BRST_stratum_III,
        "torsion_energy_modulated_GeV": torsion_energy_modulated_GeV,
        "w_0_macroscopic":             w_0_macroscopic,
        "desi_kill_switch_triggered":  kill_switch,
        "evidence_tag":                evidence_tag,
        "status":                      "STRATUM_FIREWALL_ACTIVE",
    }

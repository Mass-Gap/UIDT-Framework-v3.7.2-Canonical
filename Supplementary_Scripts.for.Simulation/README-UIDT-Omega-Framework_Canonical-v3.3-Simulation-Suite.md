UIDT Framework – Canonical v3.6.1 Simulation Suite
===================================================

<div align="center">

</div>

## Executive Summary: HMC Simulation Core

This repository provides the official **canonical** implementation of Unified Information-Density Theory (UIDT) v3.6.1. It contains a highly optimized Hybrid Monte Carlo (HMC) framework that integrates the UIDT scalar field \(S\) to verify the mass gap solution \(\Delta = 1.710\,\text{GeV}\) and the \(\gamma\)-invariant \(\gamma = 16.339\) under well-defined “Clean State” conditions (VEV = 47.7 MeV). The simulation suite constitutes a rigorous computational platform for testing the robustness and predictive power of the UIDT model against established theoretical and numerical benchmarks.

***

## 📚 Table of Contents

- Installation & Setup  
- Simulation Pipeline  
- API Reference: Core Modules  
- Empirical Predictions & Benchmarks  
- Mathematical Foundations  
- Validation & Falsification  
- Repository Tree  
- Citation  

***

## 1. Installation & Setup

To ensure reliable execution and optimal performance, the following requirements are mandatory:

- **Python version**  
  Python 3.10 or later is required to guarantee compatibility with modern scientific computing libraries and language features.

- **Hardware acceleration**  
  The suite is designed to exploit CuPy on NVIDIA GPUs (CUDA 12.x recommended).  
  - On GPU: massive parallelization of linear algebra operations and significantly reduced runtimes.  
  - On CPU: automatic fallback to NumPy for environments without CUDA; identical numerics at reduced performance.

Install the core dependencies:

```bash
pip install numpy scipy matplotlib tqdm cupy-cuda12x pytest
```

Using a dedicated virtual environment (via `venv` or `conda`) is strongly recommended to isolate dependencies and prevent version conflicts with other projects.

***

## 2. Simulation Pipeline

The simulation workflow is organized into three clearly separated phases, implemented as dedicated scripts in the `simulation/` directory.

### 2.1 Parameter Fixation

- Script: `UIDTv3.6.1_HMC-MASTER-SIMULATION.py`  
- Purpose:  
  - Analytical determination of the coupling constants \(\kappa\) and \(\lambda_S\) at fixed vacuum expectation value.  
  - Provides a consistent theoretical baseline for all subsequent simulation runs.

### 2.2 HMC Production

- Script: `UIDTv3.6.1_HMC_Optimized.py`  
- Purpose:  
  - Perform the lattice HMC simulation.  
  - Generate gauge field configurations representing the vacuum state of the theory.  
  - This phase is computationally demanding and benefits the most from GPU acceleration.

### 2.3 Diagnostics & Analysis

- Script: `UIDTv3.6.1_Hmc-Diagnostik.py`  
- Purpose:  
  - Compute mass correlators.  
  - Carry out the continuum extrapolation.  
  - Convert raw simulation data into physical observables that can be compared to experimental results and LQCD benchmarks.

***

## 3. API Reference: Core Modules

The suite is tuned for scientific precision on the order of \(\mathcal{O}(10^{-14})\) and for high-performance computing workloads. Each module fulfills a well-defined task in the overall architecture.

| Module / File                                              | Role                    | Description |
|-----------------------------------------------------------|-------------------------|-------------|
| `UIDTv3.6.1_HMC-MASTER-SIMULATION.py`                     | Parameter Fixation      | Newton–Raphson solver for determining \(\kappa\) and \(\lambda_S\) at fixed VEV \(v = 47.7\,\text{MeV}\). |
| `UIDTv3.6.1_su3_expm_cayley_hamiltonian-Modul.py`         | HPC Math Kernel         | GPU-optimized SU(3) matrix exponential via the Cayley–Hamilton theorem, crucial for efficient gauge-link updates. |
| `UIDTv3.6.1_Update-Vector.py`                             | Lattice Infrastructure  | Vectorized SU(3) link updates and gauge force computation using CuPy. |
| `UIDTv3.6.1_HMC_Optimized.py`                             | HMC Engine              | High-level control of the HMC simulation and integration of scalar field dynamics. |
| `UIDTv3.6.1_CosmologySimulator.py`                        | Cosmology               | Numerical Friedmann solver yielding \(H_0 \approx 70.4\,\text{km/s/Mpc}\); links microscopic theory to cosmological observations. |
| `UIDTv3.6.1_Lattice_Validation.py`                        | Quality Assurance       | Cross-checks numerical stability against standard routines (e.g. `scipy.linalg`). |
| `UIDTv3.6.1_Evidence_Analyzer.py`                         | Statistics              | Aggregates Z-scores to quantify the strength of empirical evidence for the theory. |
| `UIDT-3.6.1-visual.py`                                   | Visualization           | Produces final diagnostic plots and parameter figures for analysis and presentation. |

***

## 4. Empirical Predictions & Benchmarks

The credibility of a physical theory hinges on its ability to reproduce known results and to make accurate predictions. Clean State runs of UIDT v3.6.1 show excellent agreement with standard benchmarks.

| Parameter                        | UIDT v3.6.1 Value | Reference (SM / LQCD)       | Z-Score |
|----------------------------------|-------------------|-----------------------------|---------|
| Mass gap \(\Delta\)             | 1.710 GeV         | \(1710 \pm 80\) MeV         | \< 0.1  |
| Gamma \(\gamma\)                | 16.339            | Derived invariant           | Exact   |
| String tension \(\sqrt{\sigma}\)| 440 MeV           | Static potential fit        | Verified |

***

## 5. Mathematical Foundations: \(\gamma\)-Scaling

At the core of the UIDT framework lies the universal information-scaling constant \(\gamma\). This dimensionless parameter serves as a bridge between microscopic quantum-field dynamics and macroscopic observables. Unlike many parameters in effective field theory, \(\gamma\) is not fit to data; it is derived from internal consistency:

\[
\gamma = \frac{\Delta}{\sqrt{K_S}} = 16.339
\]

- \(\Delta\): Yang–Mills mass gap, the energy required to create the lightest excitation.  
- \(K_S\): kinetic vacuum expectation value, encoding the vacuum energy density.

The precise numerical value of \(\gamma\) constitutes a sharp, quantitative test of the UIDT framework.

***

## 6. Validation & Falsification Criteria

The UIDT architecture defines explicit criteria for falsification. The theory is considered falsified if any of the following conditions is satisfied:

1. **Numerics**  
   - The maximum residual in the parameter solver exceeds \(10^{-12}\).  
   - This signals a breakdown of mathematical consistency in the coupled equations.

2. **Experiment**  
   - The S-scalar is unambiguously detected outside the mass window \(1.710 \pm 0.02\,\text{GeV}\).  
   - Such a deviation would be incompatible with the strict mass prediction of UIDT.

3. **HMC**  
   - Glueball masses extracted from the lattice simulation deviate by more than \(3\sigma\) from LQCD targets.  
   - This would indicate that the UIDT modification of the Yang–Mills action does not correctly reproduce non-perturbative dynamics.

***

## 7. Repository Tree

The directory layout of the v3.6.1 Canonical Suite is designed for clarity, extensibility, and reproducibility:

```text
UIDT-Framework-V3.6.1-Canonical/
├── LICENSE.md                                      
├── README.md   (this document)
├── simulation/
│   ├── UIDTv3.6.1_HMC-MASTER-SIMULATION.py
│   ├── UIDTv3.6.1_HMC_Optimized.py
│   ├── UIDTv3.6.1_Hmc-Diagnostik.py
│   ├── UIDTv3.6.1_CosmologySimulator.py
│   ├── UIDTv3.6.1_su3_expm_cayley_hamiltonian-Modul.py
│   ├── UIDTv3.6.1_Update-Vector.py
│   ├── UIDTv3.6.1_Ape-smearing.py
│   ├── UIDTv3.6.1_Lattice_Validation.py
│   ├── UIDTv3.6.1_Evidence_Analyzer.py
│   ├── UIDTv3.6.1_Omelyna-Integrator2o.py
│   ├── UIDTv3.6.1_Monitor-Auto-tune.py
│   ├── UIDTv3.6.1_Scalar-Analyse.py
│   ├── UIDTv3.6.1_UIDT-test.py
│   └── UIDT-3.6.1-visual.py
└── Supplementary_Figures/
    ├── uidt_hmc_full_diagnostics.png
    ├── uidt_cosmology_h0.png
    ├── uidt_v3.6.1_z_scores.png
    └── balanced_string_tension.png
```

***

## 8. Cite This Work

If you use this software or the underlying theoretical framework in your research, please cite the canonical reference:

```bibtex
@article{rietz2025uidt,
  title  = {Unified Information-Density Theory (UIDT) v3.6.1: Canonical Reference (Clean State)},
  author = {Rietz, Philipp},
  year   = {2025},
  month  = {December},
  doi    = {10.5281/zenodo.17835200}
}
```

***

<div align="center">
<b>🎉 Scientific Legacy: UIDT v3.6.1 is scientifically and technically CLOSED.</b>
</div>
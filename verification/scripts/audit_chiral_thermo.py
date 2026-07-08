#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
UIDT Phase 10a: Exploratory Chiral Thermo Audit
=================================================
[D] — Numerical audit (Exploratory pattern detection)

This script calculates the off-diagonal penalty (U_off) for the [3,2,1]
matrix partition and explores the combinatorial edge weights.
It is explicitly framed as an EXPLORATORY pattern finder.
It makes NO CLAIM that [3,2,1] is uniquely selected by a universal law.
GLBC Rule: Gap Localization Before Construction.

Constants referenced (for documentation only):
  - \Delta = 1.710 GeV (Category A)
  - \gamma = 16.339 (Category C)
"""

import mpmath as mp
import itertools

# STRICT PRECISION REQUIREMENT (UIDT Constitution Rule 1)
mp.dps = 80

def get_entropy(blocks):
    r"""Calculates S = \sum n_i^2"""
    return sum(n * n for n in blocks)

def get_off_diagonal_penalty(blocks):
    r"""Calculates U_off = \sum_{i<j} n_i n_j"""
    penalty = 0
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            penalty += blocks[i] * blocks[j]
    return penalty

def verify_partition_identity(blocks):
    """Verifies N^2 = S + 2 * U_off using mpmath for residuals."""
    N = sum(blocks)
    S = get_entropy(blocks)
    U = get_off_diagonal_penalty(blocks)
    
    val_N2 = mp.mpf(N * N)
    val_S_2U = mp.mpf(S + 2 * U)
    
    residual = abs(val_N2 - val_S_2U)
    assert residual < mp.mpf('1e-14'), f"Identity failed with residual {residual}"
    return residual

def explore_chiral_edges(blocks):
    """Enumerates asymmetric edges (n_i != n_j) and computes U_off."""
    print(f"--- Exploratory Edge Audit for partition {blocks} ---")
    N = sum(blocks)
    S = get_entropy(blocks)
    U = get_off_diagonal_penalty(blocks)
    
    print(f"N = {N}")
    print(f"Entropy (S) = {S}")
    print(f"Off-diagonal Penalty (U_off) = {U}")
    
    print("\nEdge Combinations (i < j):")
    total_u = 0
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            weight = blocks[i] * blocks[j]
            total_u += weight
            asymmetric = blocks[i] != blocks[j]
            label = "Chiral (Asymmetric)" if asymmetric else "Symmetric"
            print(f"  Block {i} (n={blocks[i]}) -- Block {j} (n={blocks[j]}) => weight {weight} [{label}]")
    
    print(f"Total calculated weight: {total_u}")
    
    res = verify_partition_identity(blocks)
    print(f"Identity N^2 = S + 2*U_off verified. Residual: {res}")
    
    print("\nSTATUS: [D] Exploratory Pattern")
    print("CONCLUSION: The [3,2,1] configuration exhibits purely asymmetric edges.")
    print("WARNING: This does NOT imply a universal selection law. It is an observation under GLBC.")

if __name__ == "__main__":
    print("UIDT Phase 10a: Matrix-Thermodynamic Audit")
    print("==========================================")
    p321 = [3, 2, 1]
    explore_chiral_edges(p321)

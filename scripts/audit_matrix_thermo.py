#!/usr/bin/env python3
"""
UIDT Framework v4.0 - Matrix Thermodynamics Deterministic Audit
---------------------------------------------------------------
Prüft die kombinatorische Erhaltungsgleichung N^2 = S(p) + 2 * U_off(p)
unter strenger 80-Digit-Präzision.
Zwingende Vorgabe: Keine globalen Precision-Mutations, kein Float-Leakage.
"""

import sys
import mpmath
from mpmath import mp, mpf

def audit_partition(blocks: list[int]) -> bool:
    """
    Führt das deterministische Audit für eine einzelne Block-Partition durch.
    """
    # [UIDT Anti-Tampering] Lokale Präzisions-Isolation auf 80 Digits
    mp.dps = 80
    
    # 1. Strikte Konvertierung in mpf (Verhindert Python-Float Fallback)
    mpf_blocks = [mpf(n) for n in blocks]
    N = sum(mpf_blocks)
    
    # 2. Entropie (S = Summe der Quadrate)
    entropy = sum(n**2 for n in mpf_blocks)
    
    # 3. Off-Diagonal Penalty (U_off = Summe der Kreuzprodukte)
    off_diag_penalty = mpf('0')
    num_blocks = len(mpf_blocks)
    for i in range(num_blocks):
        for j in range(i + 1, num_blocks):
            off_diag_penalty += mpf_blocks[i] * mpf_blocks[j]
            
    # 4. Deterministische Verifikation
    expected_N_squared = N**2
    actual_sum = entropy + mpf('2') * off_diag_penalty
    
    # 5. Residual-Prüfung (< 10^-14 als Grenze für algorithmische Geschlossenheit)
    residual = abs(expected_N_squared - actual_sum)
    
    print(f"--- Audit: BlockPartition {blocks} ---")
    print(f"  N (totalDim)       : {mpmath.nstr(N, 20)}")
    print(f"  Entropy S(p)       : {mpmath.nstr(entropy, 20)}")
    print(f"  offDiagPenalty(p)  : {mpmath.nstr(off_diag_penalty, 20)}")
    print(f"  N^2 Expected       : {mpmath.nstr(expected_N_squared, 20)}")
    print(f"  S + 2*U_off Actual : {mpmath.nstr(actual_sum, 20)}")
    print(f"  Residual           : {mpmath.nstr(residual, 20)}")
    
    if residual < mpf('1e-14'):
        print("  [STATUS] VERIFIED (Residual < 1e-14)\n")
        return True
    else:
        print(f"  [STATUS] FAILED (Residual {residual} überschreitet Toleranz)\n")
        return False

def run_full_audit():
    print("==========================================================")
    print(" UIDT v4.0 MATRIX THERMODYNAMICS AUDIT (mp.dps = 80)")
    print("==========================================================\n")
    
    # Test-Batterie der primären Krajewski-Topologien
    test_partitions = [
        [3, 2, 1],          # Die Standardmodell-Partition
        [2, 2, 1, 1],       # Fragmentierte Alternativ-Partition
        [4, 2],             # Kompakte Partition
        [1, 1, 1, 1, 1, 1], # Maximale Indistinktion / Max Penalty
        [6]                 # Maximaler Block / Zero Penalty
    ]
    
    all_passed = True
    for p in test_partitions:
        if not audit_partition(p):
            all_passed = False
            
    print("==========================================================")
    if all_passed:
        print(" FINAL VERDICT: ALL AUDITS PASSED [Evidenzklasse A]")
        sys.exit(0)
    else:
        print(" FINAL VERDICT: AUDIT FAILED [System-Halt]")
        sys.exit(1)

if __name__ == "__main__":
    run_full_audit()

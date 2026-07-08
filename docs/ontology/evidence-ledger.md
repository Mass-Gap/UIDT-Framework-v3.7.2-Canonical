# UIDT Framework v4.0 - Evidence Ledger

## Meta-Axiome (Governance)
- **Repo-Axiom 1 — Keine Eigenvalidierung:** Kein Skript darf eine Größe gegen einen Wert validieren, der aus demselben Framework stammt, ohne externe Spur (Stratum III darf nie Stratum I werden).
- **Repo-Axiom 2 — Target-Leakage auf Code-Ebene:** Alle kalibrierten Werte ($\gamma$, Gap, $\delta_B$) werden hier geführt, mit explizitem Flag `solver_access = False`.
- **Repo-Axiom 3 — AI-Content niemals Evidenzklasse:** AI-generierte Texte dürfen niemals als A/B/C/D-Evidenz markiert werden, sondern bestenfalls als E (interpretiv).

## Epistemologische Axiome
- **EP-01:** Ontologischer Strukturrealismus nach Ladyman/Ross.
- **EP-02:** Kybernetischer Beobachter nach Friston/Metzinger (Active Inference).
- **EP-03:** Diskrete Relationalität als Primärdatum (Graphen-Theoretisch).
- **EP-04:** Verbot unendlicher Entropien (Rank-Budget-Theorem).

## No-Go Theoreme
1. **L7-Blockade:** Verbot von arbiträren Skalensprüngen ohne topologische Kante.
2. **Rank-Budget-Theorem [A]:** Begrenzung der Freiheitsgrade nach Frenkel-Kac. 
3. **$d^2=0$ Obstruktion:** Finale Sterbeurkunde für Arm 1 (Strict Scalar Feld).

## Claims Table (v4.0)

| Claim | Evidence Class | Stratum | Status | Reference | solver_access |
|---|---|---|---|---|---|
| $N^2 = S + 2 U_{off}$ Identity | [A] (Internal) | I (Math) | Settled | [audit_matrix_thermo.py](../../scripts/audit_matrix_thermo.py) | False |
| Standard Model Partition (3,2,1) | [C] (Calibrated) | II (Physics) | Pending | ROADMAP_S_X_FREE.md | False |
| $S(x)$ Field Rejection | [A] (No-Go) | I (Math) | Settled | EP-04, $d^2=0$ | False |

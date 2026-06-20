#!/bin/bash
# SVZ1979 -> ShifmanVainshteinZakharov1979
# Morningstar1999 -> MorningstarPeardon1999
# Add Nielsen1975 to REFERENCES.bib

sed -i 's/SVZ1979/ShifmanVainshteinZakharov1979/g' clay-submission/01_Manuscript/*.tex
sed -i 's/Morningstar1999/MorningstarPeardon1999/g' clay-submission/01_Manuscript/*.tex

# Look for Nielsen citation in main-complete.tex to get the details
grep -A 3 "Nielsen1975" clay-submission/01_Manuscript/main-complete.tex

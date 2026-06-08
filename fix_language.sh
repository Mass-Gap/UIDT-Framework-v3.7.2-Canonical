#!/bin/bash
# Language modifications

# "proves" shouldn't be altered when referring to Nielsen identities since that's a mathematical proof (gauge independence via Nielsen identities is [A] category).
# And "glueball" uses are mostly correct contextual warnings ("glueball-meson mixing obscures...") or citations.

# Let's verify if there are any other forbidden words
grep -inE "ultimate|holy grail|resolved|breakthrough|theory of everything" clay-submission/01_Manuscript/*.tex || true

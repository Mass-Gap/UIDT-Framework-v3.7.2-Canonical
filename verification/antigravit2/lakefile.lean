import Lake
open Lake DSL

package «antigravit2» where
  -- Lean 4 / mathlib4 formalization of UIDT ontological structures
  -- Evidence Tag: [D/E] — Formal software project. No physical claims.
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «Antigravit2» where
  srcDir := "Antigravit2"

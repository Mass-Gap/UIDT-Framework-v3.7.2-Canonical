import Mathlib.Data.List.Basic

def enumPartitionsBounded : ℕ → ℕ → List (List ℕ)
| 0, _ => [[]]
| _+1, 0 => []
| n+1, k+1 =>
    let m := min (n+1) (k+1)
    ((List.range' 1 m).reverse).bind fun part =>
      (enumPartitionsBounded ((n+1) - part) part).map (fun rest => part :: rest)

def enumPartitions (N : ℕ) : List (List ℕ) :=
  enumPartitionsBounded N N

example : enumPartitions 4 = [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]] := by decide

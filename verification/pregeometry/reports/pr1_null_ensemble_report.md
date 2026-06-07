# PR-1 Null-Ensemble Separation Report

Status: advisory software benchmark report for a separate experimental pregeometry workspace.

## Claims Table

| Claim | Status | Boundary |
|---|---:|---|
| Exact PR-0 integer invariants were reproduced for this executed software path. | [A] | Software path only. |
| Null-ensemble separation metrics were computed. | [D] | Distinguishability from selected nulls only. |
| Physical interpretation of the benchmark remains limited. | [D/E] | Outside PR-1 scope. |

## Reproduction Note

```powershell
py -m verification.pregeometry.experiments.run_pr1_null_ensembles --iterations 8 --seed 39 --ensemble-size 128
```

## PR-0 Toy Final Invariants

| N | E | C | beta_1 |
|---:|---:|---:|---:|
| 7 | 7 | 1 | 1 |

## Registered Metric Results

| Ensemble | Members | Final L1 mean | Trajectory L1 mean | Wasserstein mean | Permutation p |
|---|---:|---:|---:|---:|---:|
| erdos_renyi | 128 | 9.578125 | 35.59375 | 4.353515625 | 0.007751937984 |
| random_dag | 128 | 8.90625 | 34.71875 | 4.263671875 | 0.007751937984 |
| degree_preserving_shuffle | 128 | 0 | 0 | 0 | 1 |
| preferential_attachment | 128 | 2 | 6 | 0.75 | 0.007751937984 |

## Negative Results And Limitations

A nonzero distance is only a software distinguishability statement against the selected null ensembles.
Physical interpretation remains outside the scope of this benchmark.
Post-hoc metric selection is not used; the registered metric list is fixed in `PRE_REGISTERED_PR1_METRICS.md`.

## Machine Summary

```json
{
  "interpretation_boundary": "Nonzero separation means distinguishability from selected nulls only; all physical interpretation remains [D/E].",
  "metrics": [
    {
      "bootstrap_ci": {
        "high": {
          "decimal": "36.40625",
          "denominator": 32,
          "numerator": 1165
        },
        "low": {
          "decimal": "34.5625",
          "denominator": 16,
          "numerator": 553
        }
      },
      "claim_status": "[D]",
      "ensemble": "erdos_renyi",
      "final_state_l1_mean": {
        "decimal": "9.578125",
        "denominator": 64,
        "numerator": 613
      },
      "interpretation_boundary": "distinguishability from selected nulls only",
      "member_count": 128,
      "permutation_p_value": {
        "decimal": "0.007751937984",
        "denominator": 129,
        "numerator": 1
      },
      "trajectory_l1_mean": {
        "decimal": "35.59375",
        "denominator": 32,
        "numerator": 1139
      },
      "wasserstein_mean": {
        "decimal": "4.353515625",
        "denominator": 512,
        "numerator": 2229
      }
    },
    {
      "bootstrap_ci": {
        "high": {
          "decimal": "35.75",
          "denominator": 4,
          "numerator": 143
        },
        "low": {
          "decimal": "33.734375",
          "denominator": 64,
          "numerator": 2159
        }
      },
      "claim_status": "[D]",
      "ensemble": "random_dag",
      "final_state_l1_mean": {
        "decimal": "8.90625",
        "denominator": 32,
        "numerator": 285
      },
      "interpretation_boundary": "distinguishability from selected nulls only",
      "member_count": 128,
      "permutation_p_value": {
        "decimal": "0.007751937984",
        "denominator": 129,
        "numerator": 1
      },
      "trajectory_l1_mean": {
        "decimal": "34.71875",
        "denominator": 32,
        "numerator": 1111
      },
      "wasserstein_mean": {
        "decimal": "4.263671875",
        "denominator": 512,
        "numerator": 2183
      }
    },
    {
      "bootstrap_ci": {
        "high": {
          "decimal": "0",
          "denominator": 1,
          "numerator": 0
        },
        "low": {
          "decimal": "0",
          "denominator": 1,
          "numerator": 0
        }
      },
      "claim_status": "[D]",
      "ensemble": "degree_preserving_shuffle",
      "final_state_l1_mean": {
        "decimal": "0",
        "denominator": 1,
        "numerator": 0
      },
      "interpretation_boundary": "distinguishability from selected nulls only",
      "member_count": 128,
      "permutation_p_value": {
        "decimal": "1",
        "denominator": 1,
        "numerator": 1
      },
      "trajectory_l1_mean": {
        "decimal": "0",
        "denominator": 1,
        "numerator": 0
      },
      "wasserstein_mean": {
        "decimal": "0",
        "denominator": 1,
        "numerator": 0
      }
    },
    {
      "bootstrap_ci": {
        "high": {
          "decimal": "6",
          "denominator": 1,
          "numerator": 6
        },
        "low": {
          "decimal": "6",
          "denominator": 1,
          "numerator": 6
        }
      },
      "claim_status": "[D]",
      "ensemble": "preferential_attachment",
      "final_state_l1_mean": {
        "decimal": "2",
        "denominator": 1,
        "numerator": 2
      },
      "interpretation_boundary": "distinguishability from selected nulls only",
      "member_count": 128,
      "permutation_p_value": {
        "decimal": "0.007751937984",
        "denominator": 129,
        "numerator": 1
      },
      "trajectory_l1_mean": {
        "decimal": "6",
        "denominator": 1,
        "numerator": 6
      },
      "wasserstein_mean": {
        "decimal": "0.75",
        "denominator": 4,
        "numerator": 3
      }
    }
  ],
  "parameters": {
    "ensemble_size": 128,
    "ensembles": [
      "erdos_renyi",
      "random_dag",
      "degree_preserving_shuffle",
      "preferential_attachment"
    ],
    "iterations": 8,
    "seed": 39
  },
  "pr0_toy": {
    "final_invariants": {
      "C": 1,
      "E": 7,
      "N": 7,
      "beta_1": 1
    },
    "trace": [
      {
        "C": 1,
        "E": 0,
        "N": 1,
        "beta_1": 0
      },
      {
        "C": 1,
        "E": 1,
        "N": 2,
        "beta_1": 0
      },
      {
        "C": 1,
        "E": 2,
        "N": 3,
        "beta_1": 0
      },
      {
        "C": 1,
        "E": 3,
        "N": 4,
        "beta_1": 0
      },
      {
        "C": 1,
        "E": 4,
        "N": 5,
        "beta_1": 0
      },
      {
        "C": 1,
        "E": 5,
        "N": 5,
        "beta_1": 1
      },
      {
        "C": 1,
        "E": 6,
        "N": 6,
        "beta_1": 1
      },
      {
        "C": 1,
        "E": 7,
        "N": 7,
        "beta_1": 1
      }
    ]
  },
  "schema": "uidt-pregeometry-pr1-null-ensembles-v1",
  "scientific_status": {
    "null_model_separation_metrics": "[D]",
    "physical_interpretation": "[D/E]",
    "software_invariants": "[A] only for the executed software path"
  },
  "workspace_boundary": "separate experimental pregeometry workspace"
}
```

import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath('verification/prereg/PR-B1'))

from eval.validation import validate_triplet
from config import CANDIDATE_SET_P

res1 = validate_triplet("[1:1:1]", CANDIDATE_SET_P["[1:1:1]"], 16, 0.01, 1)
print("1:1:1 ->", res1)

res2 = validate_triplet("[1:2:3]", CANDIDATE_SET_P["[1:2:3]"], 16, 0.01, 1)
print("1:2:3 ->", res2)

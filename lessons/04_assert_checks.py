"""Lesson 4 - Use assert as a safety net after cleaning."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.cleaning import assert_dtype, clean_currency

# The basics
assert 1 + 1 == 2  # passes silently
try:
    assert 1 + 1 == 3
except AssertionError:
    print("assert 1 + 1 == 3 raised AssertionError, as expected")

sales = pd.read_csv(ROOT / "data" / "mpesa_sales.csv", dtype={"postal_code": str})

# Before cleaning, the check fails
try:
    assert_dtype(sales, "amount", "int64")
except AssertionError as err:
    print("Before cleaning ->", err)

# After cleaning, it passes
sales["amount"] = clean_currency(sales["amount"])
assert_dtype(sales, "amount", "int64")
assert pd.api.types.is_string_dtype(sales["postal_code"])  # "object" on pandas 2, "str" on pandas 3
assert sales["amount"].min() > 0, "amounts must be positive"
print("After cleaning -> all checks passed")
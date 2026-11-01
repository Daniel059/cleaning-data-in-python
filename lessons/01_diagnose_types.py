"""Lesson 1 - Diagnose: what type does pandas think each column is?"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "mpesa_sales.csv"

sales = pd.read_csv(DATA)

print("--- dtypes ---")
print(sales.dtypes)

print("\n--- info() ---")
sales.info()

# The trap: 'amount' is text, so sum() glues strings together.
print("\n--- summing a text column ---")
print(sales["amount"].head(3).sum())

# Another trap: postal codes read as numbers lose their leading zeros.
print("\n--- postal_code as int vs str ---")
print(sales["postal_code"].head(3).tolist())
as_text = pd.read_csv(DATA, dtype={"postal_code": str})
print(as_text["postal_code"].head(3).tolist())
"""Lesson 3 - Numbers that are really categories."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.cleaning import label_codes, to_category

DATA = ROOT / "data" / "mpesa_sales.csv"
PAYMENT_LABELS = {0: "Cash", 1: "M-Pesa", 2: "Card", 3: "Credit"}

sales = pd.read_csv(DATA, dtype={"postal_code": str})

print("--- payment_code stored as int ---")
print(sales["payment_code"].describe())

as_category = to_category(sales, ["payment_code"])
print("\n--- after converting to category ---")
print("dtype:", as_category["payment_code"].dtype)
print(as_category["payment_code"].describe())
print("\nOriginal untouched:", sales["payment_code"].dtype)

sales["payment_method"] = label_codes(sales["payment_code"], PAYMENT_LABELS)
print("\n--- readable labels ---")
print(sales[["order_id", "payment_code", "payment_method"]].head())
print()
print(sales["payment_method"].value_counts())
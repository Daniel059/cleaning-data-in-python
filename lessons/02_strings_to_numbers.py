"""Lesson 2 - Fix: strings to numbers, one stage at a time."""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "mpesa_sales.csv"

# Load postal_code as text so we don't damage it again
sales = pd.read_csv(DATA, dtype={"postal_code": str})

# Attempt 1: convert straight away (this should fail)
try:
    sales["amount"].astype("int")
except ValueError as err:
    print("Direct conversion failed:", err)

# Stage 1: remove the currency label
amount = sales["amount"].str.replace("KES ", "", regex=False)
print("\nAfter removing 'KES ':", amount.head(3).tolist())

# Stage 2: remove the thousands separator
amount = amount.str.replace(",", "", regex=False)
print("After removing ',':", amount.head(3).tolist(), "-> dtype:", amount.dtype)

# Stage 3: convert to integer
amount = amount.astype("int")
print("After astype('int'):", amount.dtype)

# Stage 4: save it back and prove it worked
sales["amount"] = amount
assert sales["amount"].dtype == "int64"

# Now real analysis is possible
print("\nTotal revenue: KES", f"{sales['amount'].sum():,}")
print("\nRevenue per county:")
print(sales.groupby("county")["amount"].sum().sort_values(ascending=False))
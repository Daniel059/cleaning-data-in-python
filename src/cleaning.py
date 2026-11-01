"""Reusable helpers for fixing data type problems in pandas."""

from __future__ import annotations

import pandas as pd


def clean_currency(series: pd.Series, prefix: str = "KES") -> pd.Series:
    """Turn strings such as "KES 1,250" into numbers (1250).

    Steps: drop the currency label, drop thousands separators, trim spaces,
    then convert. Returns an int column when every value is whole, otherwise float.
    """
    cleaned = (
        series.astype(str)
        .str.replace(prefix, "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    numbers = pd.to_numeric(cleaned)  # raises ValueError on anything unparseable
    if (numbers % 1 == 0).all():
        return numbers.astype("int64")
    return numbers.astype("float64")
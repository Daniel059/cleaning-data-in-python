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



def to_category(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Return a copy of ``df`` with ``columns`` converted to the category dtype."""
    out = df.copy()
    for col in columns:
        out[col] = out[col].astype("category")
    return out


def label_codes(series: pd.Series, mapping: dict[int, str]) -> pd.Series:
    """Replace numeric codes with readable labels and store them as categories."""
    return series.map(mapping).astype("category")



def assert_dtype(df: pd.DataFrame, column: str, expected: str) -> None:
    """Fail loudly if ``column`` does not have the ``expected`` dtype."""
    actual = str(df[column].dtype)
    assert actual == expected, f"{column!r} is {actual}, expected {expected}"
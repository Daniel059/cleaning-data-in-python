import pandas as pd
import pytest

from src.cleaning import clean_currency


def test_clean_currency_returns_ints():
    s = pd.Series(["KES 1,250", "KES 90", "KES 12,000"])
    result = clean_currency(s)
    assert result.dtype == "int64"
    assert result.tolist() == [1250, 90, 12000]


def test_clean_currency_handles_decimals():
    s = pd.Series(["KES 10.50", "KES 3.25"])
    result = clean_currency(s)
    assert result.dtype == "float64"
    assert result.sum() == pytest.approx(13.75)


def test_clean_currency_rejects_garbage():
    with pytest.raises(ValueError):
        clean_currency(pd.Series(["KES 100", "pending"]))
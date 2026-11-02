import pandas as pd
import pytest

from src.cleaning import assert_dtype, clean_currency, label_codes, to_category


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
        


def test_sum_of_raw_strings_concatenates():
    s = pd.Series(["KES 1", "KES 2"])
    assert s.sum() == "KES 1KES 2"


def test_to_category_does_not_mutate_input():
    df = pd.DataFrame({"code": [0, 1, 1, 2]})
    out = to_category(df, ["code"])
    assert str(out["code"].dtype) == "category"
    assert df["code"].dtype == "int64"


def test_label_codes():
    s = pd.Series([0, 1, 1, 3])
    labels = label_codes(s, {0: "Cash", 1: "M-Pesa", 3: "Credit"})
    assert labels.tolist() == ["Cash", "M-Pesa", "M-Pesa", "Credit"]
    assert str(labels.dtype) == "category"


def test_assert_dtype_fails_on_mismatch():
    df = pd.DataFrame({"amount": ["KES 1"]})
    with pytest.raises(AssertionError):
        assert_dtype(df, "amount", "int64")
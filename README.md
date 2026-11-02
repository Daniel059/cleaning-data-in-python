# Cleaning Data in Python: Common Data Problems

Hands-on notes and runnable code for **Chapter 1** of DataCamp's *Cleaning Data in Python* course, starting with the lesson on **data type constraints**. Instead of reusing the course datasets, every example here uses an original, Kenyan-flavoured sales dataset, so the ideas have to be understood and not just copied.

> **Garbage in, garbage out.** If a column has the wrong data type, every sum, average and chart built on it is quietly wrong.

## Contents

- [Cleaning Data in Python: Common Data Problems](#cleaning-data-in-python-common-data-problems)
  - [Contents](#contents)
  - [What you'll learn](#what-youll-learn)
  - [Project structure](#project-structure)
  - [Getting started](#getting-started)
  - [The dataset](#the-dataset)
  - [Lesson 1: Diagnose the types](#lesson-1-diagnose-the-types)
    - [The classic trap](#the-classic-trap)
  - [Lesson 2: Strings to numbers](#lesson-2-strings-to-numbers)
    - [`strip()` vs `replace()`](#strip-vs-replace)
    - [When the data is messier than expected](#when-the-data-is-messier-than-expected)
  - [Lesson 3: Numeric or categorical?](#lesson-3-numeric-or-categorical)
  - [Lesson 4: Prove it with `assert`](#lesson-4-prove-it-with-assert)
  - [Running the tests](#running-the-tests)
  - [Cheat sheet](#cheat-sheet)
  - [Common mistakes](#common-mistakes)
  - [Roadmap](#roadmap)
  - [Acknowledgements](#acknowledgements)

## What you'll learn

- How to **diagnose** column types with `dtypes` and `info()`
- Why summing a text column glues strings together instead of adding numbers
- How to convert text like `"KES 1,250"` into real numbers
- Why codes like `payment_code = 1` should be **categories**, not integers
- Why postal codes should stay as **text**
- How to use `assert` to prove your cleaning worked
- How to test cleaning functions with `pytest`

## Project structure

```
cleaning-data-in-python/
├── data/
│   └── mpesa_sales.csv              # 10 sample orders with deliberate type problems
├── src/
│   ├── __init__.py
│   └── cleaning.py                  # reusable cleaning functions
├── lessons/
│   ├── 01_diagnose_types.py
│   ├── 02_strings_to_numbers.py
│   ├── 03_numeric_to_categorical.py
│   └── 04_assert_checks.py
├── tests/
│   ├── __init__.py
│   └── test_cleaning.py             # pytest suite for src/cleaning.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting started

```bash
git clone https://github.com/Daniel059/cleaning-data-in-python.git
cd cleaning-data-in-python

python -m venv .venv
source .venv/Scripts/activate    # Git Bash on Windows
# source .venv/bin/activate      # macOS / Linux / WSL

pip install -r requirements.txt
```

Run any lesson from the project root:

```bash
python lessons/01_diagnose_types.py
python lessons/02_strings_to_numbers.py
python lessons/03_numeric_to_categorical.py
python lessons/04_assert_checks.py
```

> **Tip:** the virtual environment only stays active in the terminal where you activated it. If you see `No module named pandas` or `No module named pytest`, activate `.venv` again.
>
> **Note:** pandas 3.x displays text columns as `str`, while pandas 2.x shows `object`. They mean the same thing in this project.

## The dataset

`data/mpesa_sales.csv` is a small, made-up set of shop orders. It is deliberately dirty:

| Column | Example | Problem |
|---|---|---|
| `amount` | `KES 1,250` | The currency label and comma make it text |
| `payment_code` | `1` | Looks numeric, but it's a category (0 Cash, 1 M-Pesa, 2 Card, 3 Credit) |
| `postal_code` | `00100` | Loses its leading zeros if read as a number |

The amounts in the CSV are wrapped in quotes (`"KES 1,250"`) because they contain a comma. Without the quotes, the comma would split the value into two columns.

## Lesson 1: Diagnose the types

The first thing to do with any dataset is ask pandas what it thinks each column is.

```python
import pandas as pd

sales = pd.read_csv("data/mpesa_sales.csv")
print(sales.dtypes)
```

```
order_id        int64
shop              str
county            str
amount            str
quantity        int64
payment_code    int64
postal_code     int64
```

`amount` is text, `payment_code` is a label stored as a number, and `postal_code` has already been damaged:

```python
print(sales["postal_code"].head(3).tolist())
# [100, 80100, 40100]        <- Nairobi's 00100 became 100

as_text = pd.read_csv("data/mpesa_sales.csv", dtype={"postal_code": str})
print(as_text["postal_code"].head(3).tolist())
# ['00100', '80100', '40100']
```

**Rule of thumb:** if you wouldn't do arithmetic on it, don't store it as a number. IDs, phone numbers and postal codes are labels, not quantities.

### The classic trap

```python
print(sales["amount"].head(3).sum())
# KES 1,250KES 3,400KES 780
```

Python "adds" strings by joining them. There is no error, just a wrong answer.

## Lesson 2: Strings to numbers

The recipe is **strip the noise, convert, verify**:

```python
amount = sales["amount"].str.replace("KES ", "", regex=False)   # 1. remove the label
amount = amount.str.replace(",", "", regex=False)               # 2. remove thousands separators
amount = amount.astype("int")                                   # 3. convert

assert amount.dtype == "int64"                                  # 4. prove it
```

Order matters. Converting first fails:

```
ValueError: invalid literal for int() with base 10: 'KES 1,250'
```

The same logic is packaged as a reusable function in `src/cleaning.py`:

```python
from src.cleaning import clean_currency

sales["amount"] = clean_currency(sales["amount"])
print(f"Total revenue: KES {sales['amount'].sum():,}")
# Total revenue: KES 40,000
```

Now real analysis works:

```python
print(sales.groupby("county")["amount"].sum().sort_values(ascending=False).head(3))
```

```
county
Nakuru         12900
Nyeri           8300
Uasin Gishu     5600
```

### `strip()` vs `replace()`

| Method | Removes characters from | Good for |
|---|---|---|
| `.str.strip("$")` | the **ends** of a string only | `"$45"`, `"45$"` |
| `.str.replace(",", "")` | **anywhere** in the string | `"1,250"`, `"KES 1,250"` |

### When the data is messier than expected

By default, `pd.to_numeric` raises an error on values it can't parse, so bad data gets noticed:

```
ValueError: Unable to parse string 'pending' at position 1
```

If you want to *find* the bad rows instead, use `errors="coerce"`, which turns them into `NaN`:

```python
pd.to_numeric(pd.Series(["500", "n/a", "1200", "pending"]), errors="coerce")
```

```
0     500.0
1       NaN
2    1200.0
3       NaN
dtype: float64
```

The result is `float64` because an integer column can't hold `NaN`. Use `coerce` to locate the problems, then decide what to do with them. Don't let it hide them.

## Lesson 3: Numeric or categorical?

`payment_code` is stored as an integer, so pandas will happily compute an "average payment method":

```python
print(sales["payment_code"].describe())
```

```
count    10.000000
mean      1.200000      <- meaningless
std       0.918937      <- meaningless
min       0.000000
max       3.000000
```

Convert it to a category and `describe()` switches to summaries that make sense:

```python
sales["payment_code"] = sales["payment_code"].astype("category")
print(sales["payment_code"].describe())
```

```
count     10
unique     4
top        1
freq       5
```

Code `1` is the most common, appearing in 5 of 10 orders. Better still, replace the codes with readable labels:

```python
from src.cleaning import label_codes

PAYMENT_LABELS = {0: "Cash", 1: "M-Pesa", 2: "Card", 3: "Credit"}
sales["payment_method"] = label_codes(sales["payment_code"], PAYMENT_LABELS)

print(sales["payment_method"].value_counts())
```

```
payment_method
M-Pesa    5
Card      2
Cash      2
Credit    1
```

## Lesson 4: Prove it with `assert`

`assert` stays silent when a condition is true and raises `AssertionError` when it is false.

```python
assert 1 + 1 == 2     # nothing happens
assert 1 + 1 == 3     # AssertionError
```

Use it as a safety net after cleaning. `assert_dtype` in `src/cleaning.py` wraps the idea in a helper with a readable error message:

```python
from src.cleaning import assert_dtype

assert_dtype(sales, "amount", "int64")            # passes only after cleaning
assert sales["amount"].min() > 0, "amounts must be positive"
```

Before cleaning, the same check fails and tells you exactly what's wrong:

```
Before cleaning -> 'amount' is object, expected int64
```

After cleaning:

```
After cleaning -> all checks passed
```

Checking types is only half the job. The `min() > 0` line checks the *values*, because a column can have the right type and still hold nonsense.

## Running the tests

```bash
python -m pytest -v
```

The suite has 7 tests covering:

- integer and decimal currency conversion
- rejecting garbage values like `"pending"`
- the string-concatenation trap
- category conversion (without changing the original DataFrame)
- code-to-label mapping
- the dtype assertion helper catching a mismatch

```
tests/test_cleaning.py::test_clean_currency_returns_ints PASSED
tests/test_cleaning.py::test_clean_currency_handles_decimals PASSED
tests/test_cleaning.py::test_clean_currency_rejects_garbage PASSED
tests/test_cleaning.py::test_sum_of_raw_strings_concatenates PASSED
tests/test_cleaning.py::test_to_category_does_not_mutate_input PASSED
tests/test_cleaning.py::test_label_codes PASSED
tests/test_cleaning.py::test_assert_dtype_fails_on_mismatch PASSED

7 passed
```

Errors are tested too. `pytest.raises(...)` makes a test pass only if the expected error occurs, which is how you prove a safety check actually catches bad input.

## Cheat sheet

| Task | Code |
|---|---|
| Check types | `df.dtypes` / `df.info()` |
| Force a type while loading | `pd.read_csv(path, dtype={"postal_code": str})` |
| Remove edge characters | `s.str.strip("$")` |
| Remove characters anywhere | `s.str.replace(",", "", regex=False)` |
| Convert type | `s.astype("int")` / `"float"` / `"category"` |
| Convert, tolerating bad values | `pd.to_numeric(s, errors="coerce")` |
| Verify a type | `assert df["col"].dtype == "int64"` |
| Verify with a clear message | `assert_dtype(df, "col", "int64")` |
| Run the tests | `python -m pytest -v` |

## Common mistakes

1. **Converting before cleaning.** `astype("int")` fails on `"1,250"`.
2. **Treating IDs as numbers.** You lose leading zeros and can accidentally average them.
3. **Using `coerce` blindly.** Failed conversions become `NaN` without warning, so count them afterwards with `cleaned.isna().sum()`.
4. **Expecting `astype("int")` to work with missing values.** It fails on `NaN`. Use `"Int64"` (capital I) for nullable integers.
5. **Writing checks that never fail.** A safety net you haven't seen fail might not be catching anything. Test the failing case too.

## Roadmap

- [x] Lesson 1: Diagnosing data types
- [x] Lesson 2: Strings to numbers
- [x] Lesson 3: Numeric vs categorical
- [x] Lesson 4: Using `assert` to verify cleaning
- [x] Tests with pytest
- [ ] Data range constraints (impossible values, future dates)
- [ ] Uniqueness constraints (finding and treating duplicates)

## Acknowledgements

Concepts follow DataCamp's *Cleaning Data in Python* course. All code, data and examples in this repo are original.
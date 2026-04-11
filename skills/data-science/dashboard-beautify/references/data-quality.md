# Data Quality Gate — Reference

A beautiful dashboard built on bad data is worse than no dashboard — it creates confident, wrong decisions.
Run these checks before any design or build work. Surface findings to the user and agree remediation before proceeding.

---

## Minimum checks — always run

### Missingness
```python
import pandas as pd

def check_missingness(df: pd.DataFrame, threshold: float = 0.05) -> pd.DataFrame:
    """Flag columns with null rate above threshold."""
    null_rate = df.isnull().mean()
    flagged = null_rate[null_rate > threshold].sort_values(ascending=False)
    return flagged.rename("null_rate").to_frame()

report = check_missingness(df)
if not report.empty:
    print("⚠️  Columns with > 5% nulls — discuss with user before proceeding:")
    print(report)
```

**What to do with missingness**:
- < 5% on non-key columns: impute or drop rows, document the decision
- 5–20%: flag to user — confirm whether nulls are structural (e.g. "not applicable") or data loss
- > 20% on a key column: do not proceed — the metric cannot be trusted

### Duplicates
```python
def check_duplicates(df: pd.DataFrame, key_cols: list[str]) -> int:
    """Return count of duplicate rows on the natural key."""
    return df.duplicated(subset=key_cols).sum()

n_dupes = check_duplicates(df, key_cols=["date", "entity_id"])
if n_dupes > 0:
    raise ValueError(f"{n_dupes} duplicate rows on natural key — resolve before building.")
```

### Outliers
```python
def flag_outliers(df: pd.DataFrame, col: str, z_threshold: float = 3.5) -> pd.DataFrame:
    """Modified Z-score method — robust to non-normal distributions."""
    median = df[col].median()
    mad = (df[col] - median).abs().median()
    modified_z = 0.6745 * (df[col] - median) / (mad + 1e-9)
    return df[modified_z.abs() > z_threshold][[col]]

outliers = flag_outliers(df, "revenue")
if not outliers.empty:
    print(f"⚠️  {len(outliers)} outlier rows in 'revenue' — confirm these are real values:")
    print(outliers)
```

Do not silently remove outliers. Confirm with the user whether they are:
- Real extreme values (keep, annotate on chart)
- Ingestion errors (remove, document)
- Structural (e.g. a system test record — filter by a known flag)

### Unit consistency
Manual check — build into a docstring or a `validate_units()` function:
```python
def validate_units(df: pd.DataFrame) -> None:
    """
    Confirm unit assumptions — update this list for every project.
    revenue:    £ GBP, thousands (i.e. 4200 = £4.2M)
    cost:       £ GBP, thousands
    percentage: 0–100 scale (not 0–1)
    """
    assert df["percentage"].max() <= 100, "Percentage column appears to be on 0–1 scale"
    assert df["revenue"].min() >= 0, "Negative revenue — check for returns or credits"
```

### Metric definitions
Before building any calculated field, confirm the definition in writing. Common traps:

| Metric | Trap | Correct question to ask |
|---|---|---|
| Active users | Does "active" mean logged in? Made a purchase? Used a feature? | Define the event that constitutes "active" and the window |
| Conversion rate | Unique users or sessions in the denominator? | Confirm denominator and deduplication logic |
| Revenue | Gross or net of refunds/returns? Including VAT? | Confirm which transaction states are included |
| Churn rate | Monthly cohort or rolling 30 days? | Confirm the observation window and denominator |

### Timezone normalisation
```python
import pytz

def normalise_timezone(df: pd.DataFrame, ts_col: str, target_tz: str = "Europe/London") -> pd.DataFrame:
    """Convert all timestamps to a single named timezone."""
    tz = pytz.timezone(target_tz)
    df[ts_col] = pd.to_datetime(df[ts_col], utc=True).dt.tz_convert(tz)
    return df
```

Always store the target timezone name in `colours.py` and reference it in chart subtitles.
Never mix aware and naive datetimes in the same dataset.

---

## Extended checks — run for production dashboards

### Value range sanity
```python
EXPECTED_RANGES = {
    "percentage":    (0, 100),
    "satisfaction":  (1, 5),
    "count":         (0, None),   # None = no upper bound
}

def check_ranges(df: pd.DataFrame, ranges: dict) -> list[str]:
    issues = []
    for col, (lo, hi) in ranges.items():
        if col not in df.columns:
            continue
        if lo is not None and df[col].min() < lo:
            issues.append(f"{col}: minimum {df[col].min()} is below expected floor {lo}")
        if hi is not None and df[col].max() > hi:
            issues.append(f"{col}: maximum {df[col].max()} exceeds expected ceiling {hi}")
    return issues
```

### Referential integrity
```python
def check_foreign_keys(df_fact: pd.DataFrame, df_dim: pd.DataFrame,
                        fact_col: str, dim_col: str) -> pd.Series:
    """Return fact rows with no matching dimension record."""
    orphans = df_fact[~df_fact[fact_col].isin(df_dim[dim_col])]
    return orphans[fact_col]
```

### Reconciliation against source of truth
Before sign-off, validate at least one key metric against an agreed reference (e.g. finance report, upstream database):

```python
SOURCE_OF_TRUTH = {
    "total_revenue_q1_2024": 4_213_500.00,   # from finance system export, agreed 2024-04-10
}

computed = df[df["quarter"] == "Q1 2024"]["revenue"].sum()
tolerance = 0.001   # 0.1%
assert abs(computed - SOURCE_OF_TRUTH["total_revenue_q1_2024"]) / SOURCE_OF_TRUTH["total_revenue_q1_2024"] < tolerance, \
    f"Revenue reconciliation failed: computed {computed:,.2f} vs agreed {SOURCE_OF_TRUTH['total_revenue_q1_2024']:,.2f}"
```

Document the reconciliation reference and date in a `VALIDATION.md` file in the project root.

---

## Data quality report template

Add this to your loader and log it on every run:

```python
def data_quality_report(df: pd.DataFrame, key_cols: list[str]) -> dict:
    return {
        "row_count":        len(df),
        "duplicate_count":  df.duplicated(subset=key_cols).sum(),
        "null_rates":       df.isnull().mean().to_dict(),
        "date_range":       (str(df["date"].min()), str(df["date"].max())) if "date" in df.columns else None,
        "generated_at":     pd.Timestamp.now(tz="UTC").isoformat(),
    }
```

Log this to your application logger on every data load. Surface it in a collapsible "Data quality" panel in the dashboard if the audience is analytical.

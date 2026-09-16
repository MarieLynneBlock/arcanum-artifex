# Worked Patterns

Small synthetic examples, not a framework. Each block is independently executable
with pandas available. Assertions demonstrate invariants; use explicit exceptions
for production gates. Adapt the stated policy, not just the column names.

## Preserve Codes and Separate Invalid from Missing

Policy: `NA` is an identifier, leading zeroes matter, blank quantity is unknown,
and a present quantity must contain 1-9 ASCII digits. The bound intentionally
avoids overflow in this small example; real bounds belong to the data contract.

```python
from io import StringIO
import pandas as pd

source = pd.read_csv(
    StringIO("code,quantity\n001,7\nNA,\n003,oops\n004,1.5\n"),
    dtype={"code": "string", "quantity": "string"},
    keep_default_na=False,
    na_values={"quantity": [""]},
)
text = source["quantity"].str.strip().replace("", pd.NA)
invalid = text.notna() & ~text.str.fullmatch(r"[0-9]{1,9}", na=False)
rejected = source.loc[invalid].assign(reason="invalid_quantity")
accepted = source.loc[~invalid].assign(quantity=text.loc[~invalid].astype("Int64"))
assert len(accepted) + len(rejected) == len(source)
assert accepted["code"].tolist() == ["001", "NA"]
assert accepted["quantity"].isna().sum() == 1
assert len(rejected) == 2
```

If valid values include fractions, signed values, locale-specific notation or
scientific notation, define a different parser. Do not remove punctuation until
the result happens to parse.

## Use a Native Anti-Join with Explicit Null Semantics

Policy: return every unmatched source row, including repeated unknown keys and
missing keys. Null dimension keys must not match null source keys; report them
separately. This uses the native anti-join available in pandas 3.

```python
import pandas as pd

source = pd.DataFrame(
    {"row_id": [1, 2, 3, 4], "entity_id": ["001", "009", None, "009"]}
).astype({"entity_id": "string"})
dimension = pd.DataFrame({"entity_id": ["001", None]}, dtype="string")
invalid_dimension = dimension.loc[dimension["entity_id"].isna()]
known_keys = dimension.loc[dimension["entity_id"].notna(), ["entity_id"]].drop_duplicates()
unmatched = source.merge(
    known_keys, on="entity_id", how="left_anti", validate="many_to_one"
)
assert unmatched["row_id"].tolist() == [2, 3, 4]
assert unmatched["entity_id"].isna().sum() == 1
assert len(invalid_dimension) == 1
```

Deduplicating this keys-only membership set is intentional. It would not be a
valid substitute for resolving conflicting payloads in an enrichment dimension.

## Keep Row Grain with a Null-Aware Group Transform

Policy: retain missing grouping keys; partial totals are permitted, but groups
with no known quantities stay unknown. Index labels deliberately differ from
row positions. A transform should align back without positional reassignment.

```python
import pandas as pd

rows = pd.DataFrame(
    {"batch": ["first", "first", "second", None], "quantity": [2, None, None, 4]},
    index=[40, 10, 90, 20],
).astype({"batch": "string", "quantity": "Int64"})
grouped = rows.groupby("batch", dropna=False, observed=True, sort=False)
result = rows.assign(
    batch_quantity=grouped["quantity"].transform("sum", min_count=1),
    batch_rows=grouped["quantity"].transform("size"),
    batch_known=grouped["quantity"].transform("count"),
)
assert result.index.equals(rows.index)
assert result.loc[40, "batch_quantity"] == result.loc[10, "batch_quantity"] == 2
assert pd.isna(result.loc[90, "batch_quantity"])
assert result.loc[20, "batch_quantity"] == 4
assert result.loc[40, "batch_rows"] == 2 and result.loc[40, "batch_known"] == 1
```

## Validate a Wide-Long Round Trip

Policy: one row per item, fixed measurement columns with the same nullable integer
dtype, missing values retained. This is structural reshaping, not aggregation.

```python
import pandas as pd

wide = pd.DataFrame(
    {"item_id": ["001", "002"], "planned": [2, None], "actual": [1, 3]}
).astype({"item_id": "string", "planned": "Int64", "actual": "Int64"})
assert wide["item_id"].is_unique and wide["item_id"].notna().all()
long = wide.melt(
    id_vars="item_id", value_vars=["planned", "actual"],
    var_name="measure", value_name="quantity",
)
assert len(long) == len(wide) * 2
assert not long.duplicated(["item_id", "measure"]).any()
restored = long.pivot(index="item_id", columns="measure", values="quantity")
restored = restored.reindex(columns=["planned", "actual"]).rename_axis(columns=None)
restored = restored.reset_index()
pd.testing.assert_frame_equal(restored, wide)
```

Do not replace a failing pivot with `pivot_table` until the required aggregation
is known. For heterogeneous measurement types, a shared value column may lose
type information; preserve a schema or reshape compatible families separately.

## Flatten Children Without Losing Parent Identity

Policy: children are lists of records; an empty list has zero children; a missing
list means unknown and is reported separately. Child order is meaningful. This
fixture is already structurally validated; validate element types on real input.

```python
import pandas as pd

parents = pd.DataFrame(
    {
        "parent_id": ["001", "002", "003"],
        "children": [[{"code": "x", "quantity": 2}, {"code": "y", "quantity": 3}], [], None],
    }
)
assert parents["parent_id"].is_unique and parents["parent_id"].notna().all()
unknown = parents.loc[parents["children"].isna(), ["parent_id"]]
known = parents.loc[parents["children"].notna()].copy()
lengths = known["children"].str.len()
empty = known.loc[lengths.eq(0), ["parent_id"]]
expanded = known.loc[lengths.gt(0)].explode("children", ignore_index=True)
expanded["child_position"] = expanded.groupby("parent_id", sort=False).cumcount()
payload = pd.json_normalize(expanded["children"].tolist()).add_prefix("child.")
children = pd.concat([expanded[["parent_id", "child_position"]], payload], axis=1)
assert len(children) == lengths.sum() == 2
assert not children.duplicated(["parent_id", "child_position"]).any()
assert len(parents) == len(unknown) + len(empty) + children["parent_id"].nunique()
assert children["child.quantity"].sum() == 5
```

Both components of the horizontal concatenation have the same RangeIndex from
the expansion. That alignment is essential: flattening against the original
parent index would mispair payloads when a parent has multiple children.

## Quarantine Ambiguous and Nonexistent Local Times

Policy: naive timestamps represent `Europe/Brussels` wall time. DST folds/gaps
are rejected until the source supplies an offset or a resolution rule. This
example requires IANA timezone data, provided by the system or `tzdata` package.

```python
import pandas as pd

raw = pd.Series(["2026-03-29 02:30", "2026-10-25 02:30", "2026-03-29 03:30"])
local = pd.to_datetime(raw, format="%Y-%m-%d %H:%M", errors="coerce")
aware = local.dt.tz_localize("Europe/Brussels", ambiguous="NaT", nonexistent="NaT")
invalid_parse = raw.notna() & local.isna()
unresolved_dst = local.notna() & aware.isna()
utc = aware.dt.tz_convert("UTC")
assert invalid_parse.sum() == 0 and unresolved_dst.sum() == 2
assert utc.iloc[2] == pd.Timestamp("2026-03-29T01:30:00Z")
```

`ambiguous="infer"` relies on ordering/context and is not a general solution for
isolated timestamps. `nonexistent="shift_forward"` changes the represented time;
use it only under an explicit rule.

## Larger Example and Adaptation

[Executable checks](../examples/wrangling_checks.py) adds deterministic revision
selection, disjoint row accounting, null-aware categorical aggregation, a guarded
dimension join and temporal matching. Run it with `python` in the target
environment; use `-W error` only as an optional strict compatibility check. The
exact command and fixture policies are in the skill entry point.
Checks include duplicate input indexes, reordered input, unused categories,
missing keys, invalid values, empty/all-invalid input, duplicate dimension keys,
null temporal keys, exact matches, stale matches and unmatched entities.

When adapting, add one counterexample for the rule changed: for example, invalid
newest revision versus valid older revision; duplicate composite keys after
normalisation; conflicting temporal starts; a match exactly at the tolerance;
or keys split across two chunks. Keep expected rows explicit. Do not interpret
passing these small fixtures as evidence that a production dataset is clean.

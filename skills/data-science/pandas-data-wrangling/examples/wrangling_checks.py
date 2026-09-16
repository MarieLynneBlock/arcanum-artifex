"""Synthetic wrangling examples with executable checks; no files or network I/O."""

import pandas as pd


def wrangle_records(raw, entities):
    """Keep the latest valid revision, enrich without fan-out, and aggregate."""
    if not raw.columns.is_unique or not entities.columns.is_unique:
        raise ValueError("Column labels must be unique")
    if raw["source_id"].isna().any() or not raw["source_id"].is_unique:
        raise ValueError("source_id must be non-null and unique")

    source = raw.reset_index(drop=True)
    quantity_text = source["quantity"].astype("string").str.strip().replace("", pd.NA)
    working = source.assign(
        record_id=source["record_id"].astype("string").str.strip().replace("", pd.NA),
        entity_id=source["entity_id"].astype("string").str.strip().replace("", pd.NA),
        updated_at=pd.to_datetime(
            source["updated_at"], format="%Y-%m-%dT%H:%M:%SZ", utc=True, errors="coerce"
        ),
    )
    issues = pd.DataFrame(
        {
            "missing_key": working[["record_id", "entity_id"]].isna().any(axis=1),
            "invalid_time": working["updated_at"].isna(),
            "invalid_quantity": quantity_text.notna()
            & ~quantity_text.str.fullmatch(r"[0-9]{1,9}", na=False),
        }
    )
    invalid = issues.any(axis=1)
    rejected = source.loc[invalid].join(issues.loc[invalid])
    valid = working.loc[~invalid].assign(
        quantity=quantity_text.loc[~invalid].astype("Int64")
    )
    valid = valid.sort_values(["record_id", "updated_at", "source_id"])
    duplicate = valid.duplicated("record_id", keep="last")
    superseded = valid.loc[duplicate].reset_index(drop=True)
    kept = valid.loc[~duplicate]

    dimension = entities.loc[:, ["entity_id", "segment"]].copy()
    dimension["entity_id"] = (
        dimension["entity_id"].astype("string").str.strip().replace("", pd.NA)
    )
    if dimension["entity_id"].isna().any() or not dimension["entity_id"].is_unique:
        raise ValueError("Dimension keys must be non-null and unique after normalisation")
    records = kept.merge(
        dimension,
        on="entity_id",
        how="left",
        validate="many_to_one",
        indicator="match_status",
        suffixes=(False, False),
    )
    grouped = records.groupby("segment", dropna=False, observed=True, sort=True)
    summary = grouped.agg(
        rows=("record_id", "size"), known_quantities=("quantity", "count")
    ).join(grouped["quantity"].sum(min_count=1).rename("quantity")).reset_index()
    return records, rejected, superseded, summary


def attach_state(events, states):
    """Attach the last state at or before an event, at most two hours old."""
    events = events.loc[:, ["event_id", "entity_id", "event_at"]].copy()
    states = states.loc[:, ["entity_id", "state_at", "state"]].copy()
    for frame, time_column in ((events, "event_at"), (states, "state_at")):
        frame["entity_id"] = (
            frame["entity_id"].astype("string").str.strip().replace("", pd.NA)
        )
        frame[time_column] = pd.to_datetime(
            frame[time_column], format="%Y-%m-%dT%H:%M:%SZ", utc=True, errors="raise"
        ).dt.as_unit("us")
        if frame[["entity_id", time_column]].isna().any().any():
            raise ValueError("Temporal keys must be non-null")
    if events["event_id"].isna().any() or not events["event_id"].is_unique:
        raise ValueError("event_id must be non-null and unique")
    if states.duplicated(["entity_id", "state_at"]).any():
        raise ValueError("Resolve competing states at the same timestamp first")
    events = events.assign(_input_order=range(len(events)))
    matched = pd.merge_asof(
        events.sort_values("event_at"),
        states.sort_values("state_at"),
        left_on="event_at",
        right_on="state_at",
        by="entity_id",
        direction="backward",
        tolerance=pd.Timedelta("2h"),
        allow_exact_matches=True,
    )
    return matched.sort_values("_input_order").drop(columns="_input_order").reset_index(drop=True)


def expect_value_error(operation):
    try:
        operation()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")


def check_records():
    raw = pd.DataFrame(
        {
            "source_id": ["s1", "s2", "s3", "s4", "s5", "s6", "s7"],
            "record_id": ["r1", "r1", "r2", "r3", "r4", "r5", "r6"],
            "entity_id": [" 001 ", "001", "002", "009", None, "001", "001"],
            "updated_at": ["2026-01-01T00:00:00Z"] * 6 + ["not-a-time"],
            "quantity": ["2", "5", "", "4", "1", "bad", "1"],
        },
        dtype="string",
        index=[9] * 7,
    )
    entities = pd.DataFrame(
        {
            "entity_id": pd.Series(["001", "002"], dtype="string"),
            "segment": pd.Categorical(["core", "edge"], categories=["core", "edge", "unused"]),
        }
    )
    original = raw.copy(deep=True)
    records, rejected, superseded, summary = wrangle_records(raw, entities)
    assert (len(records), len(rejected), len(superseded)) == (3, 3, 1)
    assert len(raw) == len(records) + len(rejected) + len(superseded)
    partitions = pd.concat([records["source_id"], rejected["source_id"], superseded["source_id"]])
    assert partitions.is_unique and set(partitions) == set(raw["source_id"])
    assert records["record_id"].is_unique
    assert records["source_id"].tolist() == ["s2", "s3", "s4"]
    assert records["quantity"].dtype == pd.Int64Dtype()
    assert records["match_status"].tolist() == ["both", "both", "left_only"]
    assert rejected[["missing_key", "invalid_time", "invalid_quantity"]].sum().tolist() == [1, 1, 1]
    assert summary["rows"].sum() == len(records)
    assert summary["quantity"].sum(min_count=1) == records["quantity"].sum(min_count=1) == 9
    assert summary.loc[summary["segment"].eq("edge"), "quantity"].isna().all()
    assert summary.loc[summary["segment"].isna(), "rows"].item() == 1
    assert not summary["segment"].eq("unused").any()
    pd.testing.assert_frame_equal(raw, original)
    shuffled = wrangle_records(raw.sample(frac=1, random_state=17), entities)
    pd.testing.assert_frame_equal(records, shuffled[0])
    pd.testing.assert_frame_equal(summary, shuffled[3])

    empty = wrangle_records(raw.iloc[:0], entities)
    assert all(frame.empty for frame in empty)
    all_invalid = wrangle_records(raw.iloc[4:], entities)
    assert all_invalid[0].empty and len(all_invalid[1]) == 3
    expect_value_error(lambda: wrangle_records(raw, pd.concat([entities, entities.iloc[:1]])))
    expect_value_error(lambda: wrangle_records(raw, entities.assign(entity_id=pd.NA)))
    expect_value_error(lambda: wrangle_records(raw.assign(source_id="duplicate"), entities))


def check_temporal():
    events = pd.DataFrame(
        {
            "event_id": ["v1", "v2", "v3", "v4", "v5", "v6"],
            "entity_id": ["001", "002", "001", "001", "009", "001"],
            "event_at": [
                "2026-01-01T03:00:00Z", "2026-01-01T01:00:00Z",
                "2026-01-01T05:00:00Z", "2026-01-01T00:00:00Z",
                "2026-01-01T01:00:00Z", "2026-01-01T01:00:00Z",
            ],
        },
        dtype="string",
    )
    states = pd.DataFrame(
        {
            "entity_id": ["001", "002", "001"],
            "state_at": [
                "2026-01-01T02:00:00Z", "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z"
            ],
            "state": ["new", "other", "old"],
        },
        dtype="string",
    )
    matched = attach_state(events, states)
    assert matched["event_id"].tolist() == events["event_id"].tolist()
    assert matched["state"].fillna("unmatched").tolist() == [
        "new", "other", "unmatched", "old", "unmatched", "old"
    ]
    age = matched["event_at"] - matched["state_at"]
    assert age.dropna().between(pd.Timedelta(0), pd.Timedelta("2h")).all()
    assert attach_state(events.iloc[:0], states).empty
    assert attach_state(events, states.iloc[:0])["state_at"].isna().all()
    expect_value_error(lambda: attach_state(events, pd.concat([states, states.iloc[:1]])))
    expect_value_error(lambda: attach_state(events.assign(event_at=pd.NA), states))


if __name__ == "__main__":
    check_records()
    check_temporal()
    print(f"PASS: record and temporal wrangling checks (pandas {pd.__version__})")
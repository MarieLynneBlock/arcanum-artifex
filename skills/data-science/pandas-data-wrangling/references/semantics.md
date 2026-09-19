# Semantic Guardrails

Read only sections relevant to the transformation. Policies below are decisions
to make, not defaults to impose on every team.

## Schema, Parsing and Missingness

- Define required, optional and unexpected columns. Reject duplicate labels
  before selection or renaming. Check renamed labels for collisions as well.
  `convert_dtypes()` is an inference aid, not a schema contract; validate the
  resulting dtypes, nullability, ranges and category domains explicitly.
- Preserve identifiers as strings at ingestion. Casting a previously inferred
  number to text cannot recover leading zeroes or digits already lost to float
  precision. Specify delimiter, encoding, decimal/thousands separators and null
  tokens for text inputs; a literal `NA` can be a valid code. With `read_csv`,
  `keep_default_na=False` plus column-specific `na_values` avoids global token
  assumptions. `low_memory=False` does not make a schema explicit or bound memory.
- Retain raw values or source-row references when parsing. For `errors="coerce"`,
  track `raw.notna() & parsed.isna()` after agreed blank/token normalisation.
  Missing, malformed, out-of-range, and non-finite values are different states.
  `isna()` does not detect infinity. Report distinct row dispositions separately
  from overlapping issue flags; do not discard the audit trail after casting.
- Use nullable `Int64`, `Float64`, `boolean` and explicit `string` when their
  semantics fit. Do not turn unknown into the text `"nan"` with a broad text cast.
  `pd.NA` propagates through comparisons; a nullable selection mask needs an
  explicit unknown policy, such as `.fillna(False)` only when unknown is to be
  excluded. Do not test missingness with `== pd.NA` or `== float("nan")`.
- For exact integers, validate syntax and bounds before casting. `to_numeric`
  can lose precision for values outside native integer bounds. Monetary amounts
  require agreed units: use bounded integer minor units or an explicit decimal
  representation, not binary floats plus a cosmetic round. Check aggregate
  overflow as well as individual-value bounds before downcasting.
- String stripping, case folding and Unicode normalisation change identity.
  Apply only authorised transformations and inspect distinct raw keys collapsing
  to one normalised key. A unique dimension becoming non-unique is a gate failure,
  not permission to keep its first row. Validate unseen values before casting to
  a fixed categorical domain: otherwise unknown categories can become missing.

## Labels, Mutation and Duplicate Resolution

- pandas aligns Series assignments and arithmetic by index labels, not current
  row position. A mask from an earlier sort/filter can be misaligned. Verify
  index equality, reindex intentionally, or merge on stable identity. Use
  `.to_numpy()` only when positional pairing has been proved; it discards labels
  and can change dtype/null representation. `.loc` is label-based, `.iloc`
  positional; resetting an index does not prove that two tables correspond.
- Duplicate indexes can cause ambiguous selection or reindexing failures.
  Preserve a source identity column before discarding an index. A local row
  ordinal is useful within one batch, but is not a reproducible precedence key
  across reordered files or partitions. Use a stable composite source key then.
- Mutate explicitly with `frame.loc[mask, column] = value` or `.assign`.
  Avoid `frame[column][mask] = value` and column-level `inplace=True` calls.
  Do not change global pandas options inside a reusable transformation.
- Separate byte-identical duplicates from revisions sharing a business key.
  Specify latest/earliest preference, source priority, null ordering and a final
  deterministic tie-breaker. Sort by that full precedence before
  `drop_duplicates(keys, keep="last")`; a stable sort alone cannot resolve equal
  precedence. Conflicting ties without a legitimate rule must fail or quarantine.
- Decide whether validation occurs before or after revision selection. Selecting
  the latest valid row can resurrect an older value when the newest is invalid;
  some contracts require rejecting the entire key instead. Retain superseded
  identities and check disjoint partitions, not just final uniqueness.

## Joins and Concatenation

1. Name every join key explicitly, including composite keys and aligned dtypes.
   Omitting `on` can accidentally join on all shared column names. Decide whether
   nulls in any key component fail, quarantine, remain unmatched, or may match.
   **pandas matches null merge keys to null merge keys**, unlike ordinary SQL
   equality joins. For SQL-like left semantics, exclude right rows with any null
   key and account for them; retain left rows with null keys as unmatched.
2. Check multiplicities before merging. Use `validate="one_to_one"`,
   `"one_to_many"`, or `"many_to_one"` as appropriate. `"many_to_many"` performs
   no uniqueness check. For matching key `key`, an inner join contributes
   `left_count[key] * right_count[key]` rows. A left join also retains unmatched
   left rows. Compute counts with the same null policy and budget skewed hot keys
   before constructing a potentially enormous result.
3. Project required columns; reject unintended overlapping non-key columns or
   choose meaningful suffixes. Add `indicator=True` for coverage. Cardinality
   validation does not prove that every key matched. A left join cannot reveal
   unused right keys; audit distinct key sets with an outer join when both-sided
   coverage is required. Separate null keys from genuinely missing foreign keys.
4. Compare row and distinct-key coverage, plus totals at a comparable grain.
   Matching rows can have null payloads, so payload nullness alone is not an
   unmatched indicator. Preserve left identity to restore the required order.
   For many-to-many joins, define the resulting pair grain and any allocation
   rule; do not claim conservation of an intentionally replicated measure.
5. On pandas 3, use `how="left_anti"` or `"right_anti"` for unmatched rows. For a
  semi join, merge against distinct opposite-side keys and keep matches; do not
  multiply rows by matching duplicate lookup keys. Preserve left duplicates
  where meaningful and still apply the chosen null policy. If adapting to
  pandas 2, emulate an anti join with an indicator and select `left_only`.
  A `map` lookup also needs a unique lookup index and separate
  unknown-key/null-value accounting.
6. Before `concat`, align schema/dtypes and decide whether missing columns are
   permitted. Outer concatenation can silently introduce nulls; `join="inner"`
   can silently discard columns. `verify_integrity=True` checks the concatenated
   axis, not business-key uniqueness; `ignore_index=True` does not validate keys.
   Accumulate batches and concatenate once when memory permits, not in a loop.

## Grouping, Reshaping and Nested Records

- Choose the grain first: `agg` reduces to groups, `transform` returns values
  aligned to original rows, `filter` retains qualifying groups. Prefer named
  aggregation and native reductions over `groupby.apply` for these cases.
- Set `dropna`, `observed` and ordering intentionally. `dropna=False` retains null
  grouping keys; `observed=True` omits unobserved categorical groups. Use explicit
  reindexing against an agreed domain when zero-row groups must appear. `sort`
  controls group ordering, not chronological order inside each group.
- `size` counts rows; `count` counts non-null values. `sum(min_count=1)` preserves
  all-missing groups instead of inventing zero. Keep row and valid-value counts
  with partial aggregates. Define whether a partially missing group may have a
  partial total, or must remain unknown. Do not average group averages; combine
  sums and denominators, and only combine measures with compatible units.
- `pivot` requires unique index/column pairs; `pivot_table` aggregates duplicates
  and its default mean is not a deduplication policy. Validate uniqueness before
  reshaping; set aggregation and null handling explicitly when intentional.
  For `melt`, specify `id_vars`/`value_vars`, preserve source identity, and check
  expected rows. A wide-to-long round trip can coerce heterogeneous dtypes;
  compare reconstructed values and the declared schema, not just shape.
- `explode` turns an empty list into a row with a missing value; decide whether
  that means zero children or an empty placeholder. Multi-column explosion
  requires equal per-row lengths. Sequential explosions create a Cartesian
  product; sets have nondeterministic order. Preserve parent identity and child
  position, and reconcile expected child counts. Distinguish missing from empty
  before flattening; a later null check cannot reconstruct that distinction.
- `json_normalize` flattens structure, not relationships. Specify record paths,
  parent metadata and separator; check name collisions and optional fields.
  Never zip independent child collections by position without a contract.

## Temporal Semantics

- Distinguish an instant from a local wall-clock time or date-only value.
  Use a known format and unit/origin for numeric epochs. `utc=True` converts
  aware values but **interprets naive values as UTC**; it does not discover their
  timezone. For local times, parse first, then `tz_localize` the supplied zone
  with explicit `ambiguous` and `nonexistent` policies, then `tz_convert("UTC")`.
  Keep original zone/local values if the contract needs them. Locale and DST
  ambiguity are policy questions, not reasons to silently guess or shift times.
- For `merge_asof`, reject/quarantine missing time keys, align time dtypes/zones,
  and resolve duplicate right `(entity, time)` keys explicitly. Sort both inputs
  **globally by their time merge keys**; sorting by entity then time can fail.
  On pandas 3, inferred datetime resolution can differ, including for empty
  inputs. Specify a shared unit appropriate to source precision using
  `.dt.as_unit(...)`; verify that conversion does not truncate finer values or
  overflow. Matching timezone alone is insufficient for the join dtype contract.
  Set `by`, direction, tolerance and exact-match inclusion. Preserve both clocks,
  check match age/direction and coverage, then restore left identity/order.
  `merge_asof` has no `validate` argument; perform uniqueness checks separately.
- Effective-dated intervals need more than an as-of join. For half-open
  `[valid_from, valid_to)` records, first check positive interval lengths and no
  overlaps per entity, then choose the last start at/before the event and require
  `event_time < valid_to` (or a contractually open end). Account for gaps; never
  assume the most recent start still describes an active interval. Historical
  arrival time and effective time are different dimensions when revisions exist.
- Before `shift`, `diff`, rolling, or filling, sort within entity and resolve
  timestamp ties. Row-count windows and elapsed-time windows are not equivalent.
  Specify `min_periods`, window boundary inclusion, and alignment. For resampling,
  set `closed`, `label`, timezone and, where relevant, `origin`/`offset`; local
  days can be 23 or 25 hours. `asfreq` reindexes; resampling aggregates.
- Never forward-fill across entities. `ffill(limit=...)` limits consecutive rows,
  not elapsed time. Enforce an age bound using the last valid timestamp when
  staleness matters. Backfill/interpolation require a supplied semantic rule;
  they can borrow future values or bridge meaningful gaps.

## Memory, Chunking and Version Boundaries

- Measure `memory_usage(deep=True)` for retained data and peak process memory for
  operations; they are not interchangeable. Project columns and filter early
  only when doing so preserves semantics and required reject accounting.
  Vectorised string operations may still allocate large temporaries. Benchmark
  a representative slice including skew, long strings and realistic null density.
- Categories help repeated labels, not automatically high-cardinality IDs.
  Arrow-backed dtypes require an appropriate optional dependency and may change
  operation support or conversion behaviour. Do not impose either on all teams.
- Chunking is valid only with correct boundary state. Sums/counts can be combined
  with valid-value counts and overflow checks; means need sums and denominators.
  Exact medians, distinct counts and global deduplication are not independently
  reducible without additional state. Joins need a complete lookup or correct
  partitioning; temporal matching/filling/windows need boundary history and
  ordering. Per-chunk `drop_duplicates` does not ensure global uniqueness.
- Compare chunked and full results on keys crossing chunk boundaries before using
  the chunked implementation. If peak intermediates cannot fit, report the memory
  boundary and propose a bounded/partitioned operation or another engine with
  explicit approval. Do not turn this skill into a distributed-compute migration.
- Target pandas 3.0.5 and record the actual version/backend. Copy-on-Write is the
  only mode in pandas 3: chained assignment cannot update the parent. Do not add
  `copy=` arguments as a memory optimisation; many such arguments are ignored or
  deprecated under CoW. Derived objects can share buffers until a write; large
  retained intermediates can still drive peak memory.
- pandas 3 infers `str` with `NaN` missing semantics; explicit `string` uses
  `pd.NA`. These are not interchangeable boolean/null contracts. This package
  explicitly chooses `string` for nullable identifiers. Avoid selecting all text
  columns solely with `select_dtypes(include="object")`, and test the resulting
  masks if migrating inferred dtypes. Do not assume Arrow storage is installed.
- Categorical grouping defaults to `observed=True` in pandas 3; keep explicit
  arguments where they communicate the intended output domain. Avoid dependence
  on implicit datetime resolution or version-sensitive `groupby.apply` output.
  Adapt older-team code locally and revalidate; do not suppress dependency
  warnings globally or upgrade their environment without approval.

## Verification Menu

Choose relevant cases, not an obligatory suite for every one-line edit: empty and
all-invalid input; all-null/partially-null measures; null and duplicate composite
keys; duplicate labels; unexpected categories; unmatched dimension rows; equal
precedence conflicts; reordered input/index; malformed and out-of-range tokens;
DST gaps/folds; temporal gaps/ties/tolerance edges; variable child lengths; chunk
boundaries. Test idempotence only for operations whose contract promises it.

For a written output, read a small result back with the intended reader and check
schema, nulls, identifiers, timestamp precision and index policy. CSV does not
preserve dtypes; Parquet needs a compatible engine and still warrants a round-trip
check. Do not use pickle to exchange untrusted tables. Never overwrite a source
or publish rejects containing sensitive data without an agreed destination.

## API Sources

Bundled guidance is sufficient offline; consult documentation matching the
installed version when a behaviour is uncertain:
[merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html),
[merge_asof](https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html),
[groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html),
[Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html),
[pandas 3.0 changes](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html).

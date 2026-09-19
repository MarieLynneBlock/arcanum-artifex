---
name: pandas-data-wrangling
description: >-
  Use when cleaning, typing, filtering, deduplicating, joining, aggregating,
  reshaping, or time-aligning tabular data with pandas, or debugging row loss,
  join fan-out, null handling, index alignment, schema drift, and wrangling
  memory use. Produces explicit data contracts, reproducible transformations,
  reject accounting, and invariant checks. Data wrangling only, not exploratory
  analysis, modelling, feature engineering, visualisation, or orchestration.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: '1.0.0'
---

# Pandas Data Wrangling

Turn source tables into correctly typed, reconciled tables with a defined row
grain. Work in the team's existing notebook or module and dependency environment.
Use pandas and its testing utilities; do not introduce a validation framework,
project scaffold, or wrapper library for a task that pandas already handles.

**Target: pandas 3.0.5.** Use pandas 3 semantics and APIs as the primary path.
Confirm the consuming environment's version; do not silently upgrade it. For an
older team environment, adapt only the affected operation and validate there,
rather than adding compatibility branches throughout the skill.

## Scope

In scope: tabular ingestion/export semantics, schema alignment, parsing, missing
values, duplicate resolution, relational and temporal joins, grouping, reshaping,
nested-record flattening, and correctness-preserving performance improvements.
Profiling is limited to facts needed to wrangle correctly, such as key
multiplicity, parse failures, null counts, and memory use.

Do not expand into statistical analysis, outlier treatment without a supplied
rule, model preparation, feature selection, plotting, deployment, or pipeline
orchestration. If a request mixes these, complete the wrangling portion and state
the boundary.

## Workflow

1. **Establish the contract.** Inspect the relevant transformation and a small,
   representative input, not the whole dataset by default. Identify input and
   output grain, keys, required columns/dtypes, units, null meanings, time zones,
   expected row-count changes, and ordering. Reuse supplied rules; ask only about
   unresolved choices that would change results. Do not invent a deduplication,
   imputation, locale, timezone, or unmatched-row policy. Pending that decision,
   inspect and propose; do not silently publish a lossy result.
2. **Collect discriminating evidence.** Record pandas version and relevant dtype
   backend. Check duplicate column/index labels, key nulls and multiplicities,
   parse failure counts, and projected memory at the operation at risk. Locate a
   tiny counterexample: a duplicate key, missing group, conflicting revision,
   mixed offset, or shuffled index. Use synthetic/redacted examples in responses;
   never dump sensitive records or identifiers into logs.
3. **Implement the smallest explicit transformation.** Preserve source identity
   before filtering, sorting, joining, or exploding. Separate parsing failures
   from genuine missing values. Use native column/group operations, staged
   intermediates and `.loc`/`.assign`; do not depend on chained assignment or
   notebook execution history. Follow the operation-specific checks below.
4. **Reconcile each grain change.** Account for retained, rejected, superseded,
   unmatched, and expanded rows without double-counting. Partition counts must
   add up; overlapping issue counts need not. For joins and aggregates, reconcile
   keys and comparable measures as well as row counts. Stop on unexpected loss,
   multiplication, precision loss, or ambiguity; never repair these by blindly
   dropping duplicates, filling nulls, or coercing all columns.
5. **Verify and hand over.** Run focused checks in the consuming environment.
   Check schemas, dtypes, key uniqueness, null/domain constraints, relevant totals,
   ordering, and input non-mutation. Exercise the edge cases appropriate to the
   touched operation. Use `pd.testing.assert_frame_equal` for expected tables;
   specify tolerances only for genuinely approximate values. Use explicit
   exceptions for production gates: Python `assert` can be disabled. State what
   ran, what remains unverified, and unresolved assumptions.

For a small task, a few assertions and a short assumption note suffice. For a
multi-stage task, use this compact contract in the existing work product, not a
new mandatory document:

```text
Grain and keys: input -> output; uniqueness and permitted null keys
Schema: required/extra columns, dtypes/backend, units, null tokens, timezone
Policies: parse failures; duplicate precedence/ties; join coverage/cardinality
Shape and order: expected loss/expansion; stable identity and output ordering
Checks: partitions, key coverage, conserved measures, tolerances, edge cases
```

## Operation Gates

| Operation | Required decision and check |
| --- | --- |
| Parse or normalise | Specify accepted forms and null tokens; count new nulls and normalisation collisions; preserve raw evidence. |
| Filter or fill | Resolve nullable boolean masks; distinguish unknown from false/zero; constrain filling to permitted entities and time gaps. |
| Deduplicate | Define identity and total precedence, including ties and null timestamps; keep superseded/rejected counts. |
| Join or concatenate | Name keys, null policy, schema and expected cardinality; use `validate` and coverage checks; budget expansion before allocation. |
| Group or reshape | State output grain; set null/category semantics; reconcile counts and totals; reject accidental pivot duplicates. |
| Temporal alignment | Define clock/timezone, direction, tolerance and boundary inclusion; resolve competing timestamps; check match age and coverage. |
| Optimise | Establish a correct baseline; compare values/dtypes/order on adversarial inputs, plus measured elapsed time and peak memory. |

## Load Only What Is Needed

| Resource | Use for |
| --- | --- |
| [Semantic guardrails](./references/semantics.md) | Subtle parsing, alignment, join, grouping, temporal, chunking and version-dependent behaviour. |
| [Worked patterns](./references/patterns.md) | Small executable examples of null-safe ingestion, transforms, reshape round trips, nested rows and DST handling. |
| [Executable checks](./examples/wrangling_checks.py) | One self-contained synthetic example: reject accounting, deterministic revisions, validated enrichment, null-aware aggregation and backward as-of matching. |

## Example Checks

The skill needs no installation. The optional example uses only pandas and the
Python standard library, creates no files, accesses no network, and includes its
own checks. From this skill folder, with the team's existing Python environment:

```sh
python examples/wrangling_checks.py
```

After it passes, `python -W error examples/wrangling_checks.py` is an optional
strict compatibility check. Investigate warnings from dependencies separately;
they are environment signals, not failed data invariants. Do not run the example
with `python -O`, which disables its `assert` checks.

It deliberately uses a sample policy, not a universal business rule: `record_id`
and `entity_id` retain leading zeroes and ignore surrounding whitespace;
`source_id` and `event_id` remain exact identifiers; blank quantity is unknown;
quantities are 1-9 ASCII digits; invalid revisions are quarantined before
selecting the latest valid revision; equal timestamps are resolved by the
greatest immutable source ID. Unmatched entities remain visible. Temporal matches
allow exact timestamps and are at most two hours old; both clocks use UTC
microseconds. Replace these choices with the consuming team's contract.

Use the code as an example, not a general-purpose ingestion API. `wrangle_records`
expects `raw` columns `source_id`, `record_id`, `entity_id`, `updated_at` and
`quantity`, plus `entities` columns `entity_id` and `segment`. `attach_state`
expects `events` columns `event_id`, `entity_id` and `event_at`, plus `states`
columns `entity_id`, `state_at` and `state`. The `updated_at`, `event_at` and
`state_at` values use `YYYY-MM-DDTHH:MM:SSZ`. It provides no storage,
configuration, or dependency management.

## Response Shape

Return the transformation, its concise contract/assumptions, and an observed
validation summary: input/output grain, counts and disposition of exclusions,
join coverage, failed/passed invariants, and environment where checked. Include
only relevant evidence; do not generate a report, README, or test scaffold unless
the task needs one.

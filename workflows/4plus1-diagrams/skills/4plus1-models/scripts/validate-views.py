#!/usr/bin/env python3
"""
validate-views.py — cross-view consistency checker for 4+1 architectural documentation

Given a directory containing view markdown files (`01-logical-view.md`, `02-process-view.md`,
`03-development-view.md`, `04-physical-view.md`, `05-scenarios-view.md`), this script performs
mechanical consistency checks:

1. **Component naming consistency** — components named in the logical view should appear with
   the same names in the process, physical, and scenarios views (where exercised).
2. **No orphan components** — every component named in the logical view should be exercised by
   at least one scenario (per the coverage matrix in the scenarios view).
3. **Concern coverage** — checks that each view contains at least one `> **Concern (...):** ...`
   blockquote (indicating the architect engaged with concerns rather than skipping them).
4. **Assumption visibility** — reports how many `> **Assumption:** ...` blockquotes each view
   contains (visibility indicator — low assumptions can mean either strong context or missed
   gaps; high assumptions can mean either careful honesty or too many unknowns).

This script is deliberately conservative. It flags potential inconsistencies; it does not
fail the build. Every finding should be reviewed by a human — naming divergence is sometimes
deliberate (e.g. using a different term for the same thing because the audience reads it
differently).

Usage
-----
    python scripts/validate-views.py <path-to-view-directory>

Example
-------
    python scripts/validate-views.py examples/synth-claim/

Exit codes
----------
    0 — validation ran (with or without warnings)
    1 — fatal error (directory not found, expected files missing)
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

EXPECTED_VIEW_FILES = {
    "logical": "01-logical-view.md",
    "process": "02-process-view.md",
    "development": "03-development-view.md",
    "physical": "04-physical-view.md",
    "scenarios": "05-scenarios-view.md",
}

# Noise tokens that aren't component names even if they look like one
NOISE_TOKENS = {
    # Markdown headings that aren't components
    "Overview", "Scope", "Diagram", "Rationale", "Concerns", "Assumptions",
    "Open questions", "Related views", "Change log",
    # Generic architectural terms
    "HTTPS", "JSON", "REST", "SOAP", "mTLS", "OIDC", "VPN", "TLS",
    "AWS", "Azure", "GCP", "Kubernetes",
    # Pronouns / articles leaking into the capture
    "The", "A", "An", "This", "These", "Their",
}


@dataclass
class ViewContent:
    """Parsed content of a single view markdown file."""

    path: Path
    view_name: str
    raw_text: str
    components_mentioned: set[str] = field(default_factory=set)
    concerns_count: int = 0
    assumptions_count: int = 0
    open_questions_count: int = 0


@dataclass
class Report:
    """Accumulated validation findings."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    def emit(self) -> None:
        """Print the report to stdout, grouped by severity."""
        if self.errors:
            print("\n=== ERRORS ===")
            for e in self.errors:
                print(f"  ✗ {e}")
        if self.warnings:
            print("\n=== WARNINGS ===")
            for w in self.warnings:
                print(f"  ⚠ {w}")
        if self.info:
            print("\n=== INFO ===")
            for i in self.info:
                print(f"  ℹ {i}")
        if not (self.errors or self.warnings):
            print("\n✓ No consistency issues detected by mechanical checks.")
        print(
            f"\nTotal: {len(self.errors)} errors, "
            f"{len(self.warnings)} warnings, "
            f"{len(self.info)} informational."
        )


# -----------------------------------------------------------------------------
# Parsing helpers
# -----------------------------------------------------------------------------

def _extract_bold_component_names(text: str) -> set[str]:
    """
    Heuristic: component names are typically written in **bold** (e.g. in table
    cells and section headings). Extract all `**Foo Bar**` tokens and filter noise.
    """
    bold_tokens = set(re.findall(r"\*\*([^*]{2,80})\*\*", text))
    cleaned = set()
    for tok in bold_tokens:
        tok = tok.strip()
        if not tok:
            continue
        # Skip tokens that are clearly labels not component names
        if tok in NOISE_TOKENS:
            continue
        if tok.endswith(":"):
            tok = tok[:-1].strip()
        if tok.startswith(("Concern", "Assumption", "Decision", "Driver",
                            "Alternatives", "Consequences", "Q1", "Q2",
                            "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10",
                            "Q11", "Q12", "Q13", "Q14")):
            continue
        if tok.startswith("In scope") or tok.startswith("Out of scope"):
            continue
        # Skip pure numeric or date tokens
        if re.fullmatch(r"[0-9\-/\.: ]+", tok):
            continue
        cleaned.add(tok)
    return cleaned


def _count_blockquote_marker(text: str, marker: str) -> int:
    """Count occurrences of `> **marker...` blockquotes in the text."""
    pattern = rf">\s*\*\*{re.escape(marker)}"
    return len(re.findall(pattern, text))


def _parse_view(path: Path, view_name: str) -> ViewContent:
    raw = path.read_text(encoding="utf-8")
    return ViewContent(
        path=path,
        view_name=view_name,
        raw_text=raw,
        components_mentioned=_extract_bold_component_names(raw),
        concerns_count=_count_blockquote_marker(raw, "Concern"),
        assumptions_count=_count_blockquote_marker(raw, "Assumption"),
        open_questions_count=len(re.findall(r"\*\*Q\d+:\*\*", raw)),
    )


# -----------------------------------------------------------------------------
# Checks
# -----------------------------------------------------------------------------

def _check_files_present(root: Path, report: Report) -> dict[str, Path]:
    """Return a mapping of view_name -> path, reporting any missing files."""
    found = {}
    for view_name, filename in EXPECTED_VIEW_FILES.items():
        candidate = root / filename
        if candidate.exists():
            found[view_name] = candidate
        else:
            report.warnings.append(
                f"Expected view file not found: {filename} "
                f"(is this a partial-mode output? If so, that's OK — this check "
                f"flags it for visibility, not as an error.)"
            )
    return found


def _check_logical_components_appear_elsewhere(
    views: dict[str, ViewContent], report: Report
) -> None:
    """Components named (in bold) in the logical view should appear in at least one other view."""
    logical = views.get("logical")
    if logical is None:
        report.info.append(
            "Logical view not present — skipping component-appearance check."
        )
        return

    other_views = {k: v for k, v in views.items() if k != "logical"}
    if not other_views:
        report.info.append(
            "No other views present — cannot check component propagation."
        )
        return

    all_other_text = "\n".join(v.raw_text for v in other_views.values())
    orphans = []
    for component in sorted(logical.components_mentioned):
        # Case-insensitive substring match — a component is "mentioned" elsewhere
        # if its exact name appears (with or without bold) in any other view.
        if component.lower() not in all_other_text.lower():
            orphans.append(component)

    if orphans:
        report.warnings.append(
            "Logical-view components not mentioned in any other view "
            "(may indicate naming drift, or genuinely unexercised components): "
            + ", ".join(orphans)
        )
    else:
        report.info.append(
            f"All {len(logical.components_mentioned)} logical-view components "
            f"are mentioned elsewhere."
        )


def _check_naming_variants(views: dict[str, ViewContent], report: Report) -> None:
    """
    Look for close-but-not-identical names across views (e.g. 'Claims Service' vs
    'Claim Service'). Uses a simple normalised comparison.
    """

    def normalise(s: str) -> str:
        return re.sub(r"[\s\-_]+", "", s.lower())

    # Build a map: normalised_form -> set of actual forms seen
    variants: dict[str, set[str]] = {}
    for view in views.values():
        for comp in view.components_mentioned:
            key = normalise(comp)
            if len(key) < 3:
                continue
            variants.setdefault(key, set()).add(comp)

    found_variants = {k: v for k, v in variants.items() if len(v) > 1}
    if found_variants:
        lines = []
        for key, forms in found_variants.items():
            lines.append("  • " + " / ".join(sorted(forms)))
        report.warnings.append(
            "Possible naming variants across views (verify these are deliberate "
            "or unify):\n" + "\n".join(lines)
        )


def _check_scenarios_coverage_matrix(
    views: dict[str, ViewContent], report: Report
) -> None:
    """
    Check that the scenarios view contains a coverage matrix (markdown table
    with ✓ symbols) and that no row is entirely empty (orphan component).
    """
    scenarios = views.get("scenarios")
    if scenarios is None:
        return

    # Find markdown tables containing ✓
    tables = re.findall(
        r"((?:\|.*\|[\s]*\n)+)",
        scenarios.raw_text,
    )
    coverage_tables = [t for t in tables if "✓" in t]
    if not coverage_tables:
        report.warnings.append(
            "Scenarios view has no coverage matrix (no table with ✓ marks). "
            "Add a coverage matrix mapping components to scenarios."
        )
        return

    report.info.append(
        f"Scenarios view has {len(coverage_tables)} coverage-matrix table(s)."
    )

    # For the largest such table, check for empty rows.
    # Markdown table structure: header row, separator row (|---|---|), then data rows.
    # We skip the header (first row) and the separator row; the rest are data rows.
    largest = max(coverage_tables, key=len)
    rows = [r for r in largest.split("\n") if r.strip().startswith("|")]
    empty_rows = []
    header_seen = False
    for row in rows:
        cells = [c.strip() for c in row.split("|")[1:-1]]
        if not cells:
            continue
        # Skip separator row (all cells are dashes / colons / spaces)
        if all(re.fullmatch(r"[\-:\s]*", c) for c in cells):
            continue
        # First non-separator row = header, skip it
        if not header_seen:
            header_seen = True
            continue
        label = cells[0]
        if not label:
            continue
        body = cells[1:]
        if not any("✓" in c for c in body):
            empty_rows.append(label)

    if empty_rows:
        report.warnings.append(
            "Components in coverage matrix with no scenario ticks (orphan components): "
            + ", ".join(empty_rows)
        )


def _check_concerns_engagement(views: dict[str, ViewContent], report: Report) -> None:
    """Each view should have at least one `> **Concern (...)...` blockquote."""
    for view_name, view in views.items():
        if view.concerns_count == 0:
            report.warnings.append(
                f"View '{view_name}' has no `> **Concern (…):**` blockquotes. "
                f"Either no concerns apply (confirm this is true) or the concerns "
                f"section was skipped."
            )
        else:
            report.info.append(
                f"View '{view_name}': {view.concerns_count} concern(s) flagged."
            )


def _report_assumption_visibility(views: dict[str, ViewContent], report: Report) -> None:
    """Informational — show how many assumptions each view makes."""
    for view_name, view in views.items():
        if view.assumptions_count > 0:
            report.info.append(
                f"View '{view_name}': {view.assumptions_count} assumption(s) "
                f"flagged, {view.open_questions_count} open question(s)."
            )


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-view consistency checker for 4+1 architectural documentation."
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Path to the directory containing 01-logical-view.md ... 05-scenarios-view.md",
    )
    args = parser.parse_args()

    if not args.directory.exists():
        print(f"ERROR: directory not found: {args.directory}", file=sys.stderr)
        return 1
    if not args.directory.is_dir():
        print(f"ERROR: not a directory: {args.directory}", file=sys.stderr)
        return 1

    report = Report()
    print(f"Validating 4+1 views in: {args.directory}")

    present = _check_files_present(args.directory, report)
    if not present:
        report.errors.append("No expected view files found at all.")
        report.emit()
        return 1

    views = {
        view_name: _parse_view(path, view_name)
        for view_name, path in present.items()
    }

    for view_name, view in views.items():
        print(
            f"  Parsed {view.path.name}: "
            f"{len(view.components_mentioned)} bold tokens, "
            f"{view.concerns_count} concerns, "
            f"{view.assumptions_count} assumptions."
        )

    _check_logical_components_appear_elsewhere(views, report)
    _check_naming_variants(views, report)
    _check_scenarios_coverage_matrix(views, report)
    _check_concerns_engagement(views, report)
    _report_assumption_visibility(views, report)

    report.emit()
    return 0


if __name__ == "__main__":
    sys.exit(main())

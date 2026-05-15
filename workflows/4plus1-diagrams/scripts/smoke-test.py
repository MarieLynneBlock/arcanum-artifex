#!/usr/bin/env python3
"""Smoke test the standalone 4plus1-diagrams workflow bundle.

Checks are intentionally mechanical and fast:
- required workflow files and folders exist
- workflow, skill, and agent entry frontmatter follows required order
- relative Markdown links resolve inside the bundle
- local links do not escape the bundle root
- stale legacy references are absent
- Miro example prompt filenames follow the documented contract
- workflow-level and skill-internal Miro templates stay in sync
- draw.io templates parse and pass the vendored draw.io validator
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "WORKFLOW.md",
    "architecture-documentation.agent.md",
    "agents/architecture-documentation.agent.md",
    "prompts/4plus1-diagrams.prompt.md",
    "instructions/draw-io.instructions.md",
    "instructions/miro.instructions.md",
    "references/notation-drawio.md",
    "references/notation-miro.md",
    "skills/4plus1-models/SKILL.md",
    "skills/draw-io-diagram-generator/SKILL.md",
    "skills/miro-diagram-generator/SKILL.md",
    "skills/miro-diagram-generator/templates/miro-prompt-template.md",
    "skills/miro-diagram-generator/templates/full-board-prompt-template.md",
    "templates/miro/miro-prompt-template.md",
    "templates/miro/full-board-prompt-template.md",
    "templates/drawio/logical-view.drawio",
    "templates/drawio/process-view-sequence.drawio",
    "templates/drawio/process-view-bpmn.drawio",
    "templates/drawio/development-view.drawio",
    "templates/drawio/physical-view-aws.drawio",
    "templates/drawio/physical-view-azure.drawio",
    "templates/drawio/physical-view-generic.drawio",
    "templates/drawio/scenarios-view.drawio",
]

FORBIDDEN_TEXT = [
    ".github/skills/",
    ".github/prompts/",
    ".github/instructions/",
    "skills/architecture-models-4plus1",
    "architecture-models-4plus1/",
    "logical-view-prompt.md",
    "process-view-prompt.md",
    "development-view-prompt.md",
    "physical-view-prompt.md",
    "scenarios-view-prompt.md",
    "skills/draw-io-diagram-generator/templates/",
]

ALLOWLISTED_FORBIDDEN_CONTEXT = {
    "architecture-models-4plus1": "historical changelog wording is allowed only if it is not a path",
}

MARKDOWN_EXTENSIONS = {".md", ".agent.md", ".prompt.md", ".instructions.md"}
LOCAL_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def is_markdown(path: Path) -> bool:
    name = path.name
    return path.suffix == ".md" or name.endswith((".agent.md", ".prompt.md", ".instructions.md"))


def is_external_link(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "vscode:", "file:"))


def resolve_local_link(source: Path, target: str) -> Path | None:
    target = target.strip()
    if not target or target.startswith("#") or is_external_link(target):
        return None
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    if not target:
        return None
    target = unquote(target)
    return (source.parent / target).resolve()


def check_required_paths(errors: list[str]) -> None:
    for path_text in REQUIRED_PATHS:
        path = ROOT / path_text
        if not path.exists():
            add_error(errors, f"Required path missing: {path_text}")


def check_entry_frontmatter(errors: list[str]) -> None:
    entry_files = [ROOT / "README.md", ROOT / "WORKFLOW.md"]
    entry_files.extend(sorted(ROOT.rglob("SKILL.md")))
    entry_files.extend(sorted(ROOT.rglob("*.agent.md")))

    for path in entry_files:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) < 6:
            add_error(errors, f"Entry frontmatter too short: {rel(path)}")
            continue
        if lines[0] != "---":
            add_error(errors, f"Entry frontmatter missing opening fence: {rel(path)}")
        if not lines[1].startswith("name: "):
            add_error(errors, f"Entry frontmatter missing name as first field: {rel(path)}")
        if not lines[2].startswith("description: "):
            add_error(errors, f"Entry frontmatter missing description as second field: {rel(path)}")
        if lines[3] != "metadata:":
            add_error(errors, f"Entry frontmatter missing metadata as third field: {rel(path)}")
        if not re.match(r"^ +skill-author: ", lines[4]):
            add_error(errors, f"Entry frontmatter missing skill-author metadata: {rel(path)}")
        if "---" not in lines[5:]:
            add_error(errors, f"Entry frontmatter missing closing fence: {rel(path)}")


def check_markdown_links(errors: list[str]) -> None:
    for md_file in sorted(path for path in ROOT.rglob("*") if path.is_file() and is_markdown(path)):
        text = md_file.read_text(encoding="utf-8")
        for match in LOCAL_LINK_RE.finditer(text):
            raw_target = match.group(1).strip()
            # Drop optional Markdown title: [x](target "title")
            if " " in raw_target and not raw_target.startswith("<"):
                raw_target = raw_target.split(" ", 1)[0]
            raw_target = raw_target.strip("<>")
            resolved = resolve_local_link(md_file, raw_target)
            if resolved is None:
                continue
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                add_error(errors, f"Link escapes bundle: {rel(md_file)} -> {raw_target}")
                continue
            if not resolved.exists():
                add_error(errors, f"Broken link: {rel(md_file)} -> {raw_target}")


def check_forbidden_text(errors: list[str]) -> None:
    for path in sorted(path for path in ROOT.rglob("*") if path.is_file() and is_markdown(path)):
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                add_error(errors, f"Stale reference in {rel(path)}: {forbidden}")


def check_miro_prompt_names(errors: list[str]) -> None:
    prompt_dir = ROOT / "skills/miro-diagram-generator/examples/synth-claim/miro-prompts"
    if not prompt_dir.exists():
        add_error(errors, f"Missing Miro example directory: {rel(prompt_dir)}")
        return
    for path in sorted(prompt_dir.glob("*.md")):
        if path.name == "full-board-prompt.md":
            continue
        if not path.name.endswith("-miro-prompt.md"):
            add_error(errors, f"Miro example does not follow -miro-prompt.md naming: {rel(path)}")


# Matches bare diagrams/<word>.<ext> or diagrams/<word>-miro-prompt.md (flat, unsubfoldered paths).
# Allowed context: code-fence paths that already contain a subfolder (mermaid/, drawio/, miro/).
_FLAT_DIAGRAM_PATH_RE = re.compile(
    r"diagrams/"
    r"(?!mermaid/|drawio/|miro/)"
    r"[\w-]+\.(?:mmd|puml|drawio)"
    r"|diagrams/(?!miro/)[\w-]+-miro-prompt\.md"
)

# Files where this check is enforced (instruction and reference docs are excluded).
_OUTPUT_CONTRACT_SCOPE = {
    "README.md",
    "WORKFLOW.md",
    "architecture-documentation.agent.md",
    "agents/architecture-documentation.agent.md",
    "prompts/4plus1-diagrams.prompt.md",
    "skills/4plus1-models/SKILL.md",
    "skills/miro-diagram-generator/SKILL.md",
    "skills/draw-io-diagram-generator/SKILL.md",
}


def check_output_path_contract(errors: list[str]) -> None:
    """Ensure no file in the output contract scope uses the old flat diagrams/ paths."""
    for relative in _OUTPUT_CONTRACT_SCOPE:
        path = ROOT / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for match in _FLAT_DIAGRAM_PATH_RE.finditer(text):
            add_error(
                errors,
                f"Flat diagrams/ output path in {relative}: '{match.group()}' — "
                "use diagrams/mermaid/, diagrams/drawio/, or diagrams/miro/ instead",
            )
        _check_tree_diagram_paths(relative, text, errors)
        _check_canonical_view_filenames(relative, text, errors)


# Detects a tree line introducing the diagrams/ folder (with no trailing typed subfolder on the same line).
_TREE_DIAGRAMS_LINE_RE = re.compile(r"^[\s\u2502\u251c\u2514\u2500]*diagrams/\s*$", re.MULTILINE)
# Detects a tree leaf with a flat diagram filename and no enclosing typed subfolder context.
_TREE_LEAF_RE = re.compile(r"[\u251c\u2514]\u2500\u2500\s+([\w-]+\.(?:mmd|puml|drawio)|[\w-]+-miro-prompt\.md)")
_TYPED_SUBFOLDERS = ("mermaid/", "drawio/", "miro/")
_CANONICAL_VIEW_NAME_RE = re.compile(r"\b(\d{2})-(overview|logical-view|process-view|development-view|physical-view|scenarios-view)\.md\b")
_CANONICAL_VIEW_NAMES = {
    "00": "system-context",
    "01": "logical-view",
    "02": "process-view",
    "03": "development-view",
    "04": "physical-view",
    "05": "scenarios-view",
}


def _check_tree_diagram_paths(relative: str, text: str, errors: list[str]) -> None:
    """Within markdown trees, every diagrams/ folder must be followed by typed subfolder leaves."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not _TREE_DIAGRAMS_LINE_RE.match(line):
            continue
        # Inspect the next ~12 lines for the immediate children of this diagrams/ folder.
        # A child is a leaf at deeper indentation. Stop at blank line or fence end.
        for j in range(i + 1, min(i + 14, len(lines))):
            child = lines[j]
            if not child.strip() or child.strip().startswith("```"):
                break
            leaf_match = _TREE_LEAF_RE.search(child)
            if not leaf_match:
                continue
            # If this leaf is a bare diagram filename directly under diagrams/ (no typed subfolder above it on the path),
            # scan upward to ensure a typed subfolder line precedes it.
            ancestor_window = lines[i + 1 : j]
            if not any(sub in ancestor for ancestor in ancestor_window for sub in _TYPED_SUBFOLDERS):
                add_error(
                    errors,
                    f"Tree-style flat diagrams/ leaf in {relative}: '{leaf_match.group(1)}' — "
                    "place under diagrams/mermaid/, diagrams/drawio/, or diagrams/miro/",
                )


def _check_canonical_view_filenames(relative: str, text: str, errors: list[str]) -> None:
    """View files must use canonical 00-system-context / 01..05- naming."""
    for match in _CANONICAL_VIEW_NAME_RE.finditer(text):
        prefix, name = match.group(1), match.group(2)
        canonical = _CANONICAL_VIEW_NAMES.get(prefix)
        if canonical is None or name != canonical:
            add_error(
                errors,
                f"Non-canonical view filename in {relative}: '{match.group(0)}' — "
                "expected 00-system-context.md and 01..05-<view>.md",
            )


_VALIDATE_VIEWS_INVOCATION_RE = re.compile(r"python\s+\S*validate-views\.py(?:\s+(\S+))?")


def check_validate_views_command(errors: list[str]) -> None:
    """Wherever validate-views.py is invoked as a `python ...` command, require a positional directory argument."""
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and is_markdown(p)):
        text = path.read_text(encoding="utf-8")
        for match in _VALIDATE_VIEWS_INVOCATION_RE.finditer(text):
            arg = match.group(1)
            if arg is None or arg.startswith("`"):
                add_error(
                    errors,
                    f"validate-views.py invocation missing positional directory argument in {rel(path)}: {match.group(0)}",
                )


def check_miro_template_parity(errors: list[str]) -> None:
    template_pairs = [
        (
            ROOT / "templates/miro/miro-prompt-template.md",
            ROOT / "skills/miro-diagram-generator/templates/miro-prompt-template.md",
        ),
        (
            ROOT / "templates/miro/full-board-prompt-template.md",
            ROOT / "skills/miro-diagram-generator/templates/full-board-prompt-template.md",
        ),
    ]
    for workflow_template, skill_template in template_pairs:
        if not workflow_template.exists() or not skill_template.exists():
            continue
        if workflow_template.read_text(encoding="utf-8") != skill_template.read_text(encoding="utf-8"):
            add_error(
                errors,
                f"Miro template drift: {rel(workflow_template)} must match {rel(skill_template)}",
            )


def load_drawio_validator():
    validator_path = ROOT / "skills/draw-io-diagram-generator/scripts/validate-drawio.py"
    spec = importlib.util.spec_from_file_location("validate_drawio", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load draw.io validator from {validator_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_drawio_templates(errors: list[str]) -> None:
    try:
        validator = load_drawio_validator()
    except RuntimeError as exc:
        add_error(errors, str(exc))
        return
    # Workflow-level templates must carry canonical-source-ref provenance cells;
    # the skill-internal generic templates are not subject to that contract.
    drawio_roots = [
        (ROOT / "templates/drawio", True),
        (ROOT / "skills/draw-io-diagram-generator/assets/templates", False),
    ]
    for drawio_root, require_provenance in drawio_roots:
        if not drawio_root.exists():
            add_error(errors, f"Missing draw.io template directory: {rel(drawio_root)}")
            continue
        for drawio_file in sorted(drawio_root.glob("*.drawio")):
            validation_errors = validator.validate_file(drawio_file, require_provenance=require_provenance)
            for validation_error in validation_errors:
                add_error(errors, f"draw.io validation failed in {rel(drawio_file)}: {validation_error}")


def main() -> int:
    errors: list[str] = []
    check_required_paths(errors)
    check_entry_frontmatter(errors)
    check_markdown_links(errors)
    check_forbidden_text(errors)
    check_output_path_contract(errors)
    check_validate_views_command(errors)
    check_miro_prompt_names(errors)
    check_miro_template_parity(errors)
    check_drawio_templates(errors)

    if errors:
        print("SMOKE TEST FAIL")
        for error in errors:
            print(f"- {error}")
        print(f"\n{len(errors)} issue(s) found.")
        return 1

    print("SMOKE TEST PASS")
    print("- required files/folders present")
    print("- workflow, skill, and agent entry frontmatter follows required order")
    print("- internal Markdown links resolve inside the bundle")
    print("- no stale legacy references detected")
    print("- output paths use diagrams/mermaid/, diagrams/drawio/, diagrams/miro/ subfolders")
    print("- view filenames use canonical 00-system-context / 01..05-<view>.md form")
    print("- validate-views.py is invoked with a positional directory argument")
    print("- Miro example prompt filenames match the naming contract")
    print("- workflow and skill Miro templates are in sync")
    print("- draw.io templates passed XML validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())

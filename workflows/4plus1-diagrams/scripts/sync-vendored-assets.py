#!/usr/bin/env python3
"""Synchronise vendored workflow assets from declared bundle-local sources.

Default mode is dry-run. Use --apply to copy source content into local vendored paths.
The script reads vendored-assets-manifest.json in the workflow root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "vendored-assets-manifest.json"


def should_skip_file(path: Path) -> bool:
    parts = set(path.parts)
    if "__pycache__" in parts:
        return True
    if path.suffix in {".pyc", ".pyo"}:
        return True
    if path.name in {".DS_Store"}:
        return True
    return False


@dataclass
class DiffSummary:
    added: list[str]
    removed: list[str]
    changed: list[str]

    def has_changes(self) -> bool:
        return bool(self.added or self.removed or self.changed)


def read_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RuntimeError(f"Manifest missing: {path}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Manifest is invalid JSON: {exc}") from exc

    assets = data.get("assets")
    if not isinstance(assets, list):
        raise RuntimeError("Manifest must contain an 'assets' list")
    return data


def iter_files(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    if path.is_file():
        if should_skip_file(path):
            return {}
        rel_name = path.name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return {rel_name: digest}

    files: dict[str, str] = {}
    for file_path in sorted(p for p in path.rglob("*") if p.is_file()):
        if should_skip_file(file_path):
            continue
        rel_name = file_path.relative_to(path).as_posix()
        files[rel_name] = hashlib.sha256(file_path.read_bytes()).hexdigest()
    return files


def compute_tree_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    if path.is_file():
        if should_skip_file(path):
            return hasher.hexdigest()
        hasher.update(path.name.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        return hasher.hexdigest()

    for file_path in sorted(p for p in path.rglob("*") if p.is_file()):
        if should_skip_file(file_path):
            continue
        rel_name = file_path.relative_to(path).as_posix()
        hasher.update(rel_name.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(file_path.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def resolve_source(asset: dict[str, Any]) -> Path | None:
    source = asset.get("source", {})
    source_path = source.get("path")
    source_kind = source.get("kind")

    if not isinstance(source_path, str) or not source_path or source_path == "[TODO]":
        return None

    if source_kind == "bundle-path":
        resolved = (ROOT / source_path).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            return None
        return resolved
    return None


def copy_asset(source: Path, dest: Path) -> None:
    if dest.exists():
        if dest.is_file() or dest.is_symlink():
            dest.unlink()
        else:
            shutil.rmtree(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    if source.is_file():
        shutil.copy2(source, dest)
    else:
        shutil.copytree(source, dest)


def diff_paths(source: Path, dest: Path) -> DiffSummary:
    source_files = iter_files(source)
    dest_files = iter_files(dest)

    added = sorted(name for name in source_files.keys() - dest_files.keys())
    removed = sorted(name for name in dest_files.keys() - source_files.keys())
    changed = sorted(
        name
        for name in source_files.keys() & dest_files.keys()
        if source_files[name] != dest_files[name]
    )
    return DiffSummary(added=added, removed=removed, changed=changed)


def print_diff(asset_id: str, source: Path, dest: Path, diff: DiffSummary) -> None:
    print(f"[{asset_id}]")
    print(f"  source: {source}")
    print(f"  local : {dest}")
    print(
        "  diff  : "
        f"{len(diff.added)} added, {len(diff.changed)} changed, {len(diff.removed)} removed"
    )


def limit_list(items: list[str], max_items: int = 20) -> list[str]:
    if len(items) <= max_items:
        return items
    hidden = len(items) - max_items
    return items[:max_items] + [f"... (+{hidden} more)"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync vendored assets from manifest sources inside this bundle"
    )
    parser.add_argument("--apply", action="store_true", help="Apply changes instead of dry-run")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicit dry-run mode (default behavior when --apply is not set).",
    )
    parser.add_argument(
        "--asset",
        action="append",
        default=[],
        help="Only process asset id(s) from manifest. Repeat for multiple assets.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat missing, TODO, non-bundle, or out-of-bundle sources as errors.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = read_manifest(MANIFEST_PATH)
    assets = data["assets"]

    if args.asset:
        selected = set(args.asset)
        assets = [a for a in assets if a.get("id") in selected]
        missing_ids = sorted(selected - {a.get("id") for a in assets})
        for missing in missing_ids:
            print(f"[error] unknown asset id in --asset: {missing}")
        if missing_ids:
            return 2

    blocked = 0
    changed_assets: list[dict[str, Any]] = []

    print("Mode:", "apply" if args.apply else "dry-run")
    print(f"Manifest: {MANIFEST_PATH}")

    for asset in assets:
        asset_id = asset.get("id", "<unknown>")
        local_rel = asset.get("local_path")
        if not isinstance(local_rel, str):
            print(f"[error] {asset_id}: missing local_path")
            blocked += 1
            continue

        source_path = resolve_source(asset)
        local_path = (ROOT / local_rel).resolve()

        if source_path is None:
            print(f"[blocked] {asset_id}: source.path is missing, TODO, outside bundle, or source.kind is not bundle-path")
            blocked += 1
            continue

        if not source_path.exists():
            print(f"[blocked] {asset_id}: source path does not exist: {source_path}")
            blocked += 1
            continue

        diff = diff_paths(source_path, local_path)
        print_diff(asset_id, source_path, local_path, diff)

        if diff.added:
            print("    +", ", ".join(limit_list(diff.added)))
        if diff.changed:
            print("    ~", ", ".join(limit_list(diff.changed)))
        if diff.removed:
            print("    -", ", ".join(limit_list(diff.removed)))

        if not diff.has_changes():
            continue

        changed_assets.append(asset)
        if args.apply:
            copy_asset(source_path, local_path)
            asset.setdefault("integrity", {})["algo"] = "sha256-tree-v1"
            asset["integrity"]["hash"] = compute_tree_hash(local_path)
            asset["last_sync_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            print(f"    applied changes to {local_rel}")

    if args.strict and blocked:
        print(f"\nSync failed: {blocked} blocked asset(s).")
        return 2

    if args.apply:
        data["generated_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        MANIFEST_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print("\nManifest updated.")

    print(
        f"\nSummary: {len(changed_assets)} asset(s) with changes, "
        f"{blocked} blocked asset(s), mode={'apply' if args.apply else 'dry-run'}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

---
name: agent-supply-chain
description: >
  Review, generate, and verify supply-chain integrity controls for AI agent tools, plugins, MCP servers, skills, prompts, and custom agents, including SHA-256 manifests, dependency pinning, provenance evidence, promotion gates, and CI verification.
metadata:
  skill-author: 'Marie-Lynne Block'
---

# Agent Supply Chain Integrity

Generate and verify integrity manifests for AI agent tools, plugins, MCP servers, skills, prompts, and custom agents. Detect unexpected file changes, enforce dependency pinning, and capture provenance evidence before promotion.

## Overview

Agent assets often combine executable code, prompts, policy files, and tool configuration. Treat them as deployable software: pin dependencies, record what was reviewed, verify the reviewed files before release, and fail closed when integrity evidence is missing.

```
Agent Asset Folder -> Hash Reviewable Files -> Generate INTEGRITY.json
        Later CI -> Re-hash Files -> Compare Hashes + Manifest Hash
        Result -> verified | modified | missing | untracked | invalid
```

This skill provides lightweight integrity controls. It does not replace signed releases, SLSA provenance, SBOM tooling, vulnerability scanning, or organisation-specific release policy.

## Use This Skill When

- Promoting an agent tool, plugin, MCP server, skill, prompt, or custom agent to a shared or production environment
- Reviewing a pull request that adds or changes agent-executable code, tool configuration, or bundled instructions
- Adding a CI gate to verify that reviewed files still match the integrity manifest
- Auditing third-party agent assets before adoption
- Checking dependency pinning, lockfiles, provenance notes, and release evidence for agentic components

## Do Not Use This Skill For

- Formal compliance claims without signed artefacts, release attestations, and organisational approval
- General application security review where agent assets and tool supply chain are not in scope
- Runtime agent governance, approval workflows, or policy enforcement design
- Vulnerability scanning of dependencies; use dedicated package and container scanners alongside this skill

---

## Review Workflow

1. Define scope: identify the asset folder, entry points, tool manifests, scripts, prompts, skills, lockfiles, and generated artefacts.
2. Decide exclusions: ignore caches, virtual environments, dependency folders, build outputs, local secrets, and the integrity manifest itself.
3. Generate `INTEGRITY.json` from reviewable source files using stable path ordering and SHA-256 file hashes.
4. Review dependency declarations for exact versions or lockfiles. Record `[TODO]` where a project-specific package manager or policy is unknown.
5. Verify the manifest before merge, release, deployment, or marketplace publication.
6. Report findings as `verified`, `modified`, `missing`, `untracked`, `unpinned`, `unknown`, or `not applicable`.

---

## Pattern 1: Generate an Integrity Manifest

Create `INTEGRITY.json` with SHA-256 hashes of all reviewable files. The `manifest_hash` binds each relative path to its file hash so that renames and path swaps are visible.

```python
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

EXCLUDE_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "node_modules",
}
EXCLUDE_FILES = {
    ".DS_Store",
    ".env",
    ".env.local",
    "INTEGRITY.json",
    "Thumbs.db",
}


def iter_reviewable_files(root: Path) -> Iterable[Path]:
    """Yield files that should be covered by the integrity manifest."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(root).parts
        if path.name in EXCLUDE_FILES:
            continue
        if any(part in EXCLUDE_DIRS for part in relative_parts):
            continue
        yield path


def hash_file(path: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_hash(files: dict[str, str]) -> str:
    """Bind relative paths and file hashes into one deterministic manifest hash."""
    digest = hashlib.sha256()
    for relative_path, file_hash in sorted(files.items()):
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def generate_manifest(asset_dir: str, asset_type: str = "agent-asset") -> dict:
    """Generate an integrity manifest for an agent asset folder."""
    root = Path(asset_dir).resolve()
    files = {}

    for path in iter_reviewable_files(root):
        relative_path = path.relative_to(root).as_posix()
        files[relative_path] = hash_file(path)

    return {
        "asset_name": root.name,
        "asset_type": asset_type,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": "sha256",
        "file_count": len(files),
        "files": files,
        "manifest_hash": manifest_hash(files),
    }


asset_path = Path("my-agent-tool")
manifest = generate_manifest(str(asset_path), asset_type="mcp-server")
(asset_path / "INTEGRITY.json").write_text(
    json.dumps(manifest, indent=2) + "\n"
)
print(f"Generated manifest: {manifest['file_count']} files, "
      f"hash: {manifest['manifest_hash'][:16]}...")
```

**Output (`INTEGRITY.json`):**
```json
{
    "asset_name": "my-agent-tool",
    "asset_type": "mcp-server",
    "generated_at": "2026-05-20T03:00:00+00:00",
  "algorithm": "sha256",
    "file_count": 4,
  "files": {
        "README.md": "e5f6a7b8...",
        "package-lock.json": "97bcda42...",
        "package.json": "a1b2c3d4...",
        "src/server.ts": "c9d0e1f2..."
  },
  "manifest_hash": "7e8f9a0b1c2d3e4f..."
}
```

---

## Pattern 2: Verify Integrity

Check that current files match the manifest.

```python
import json
from pathlib import Path


# Requires: generate_manifest(), hash_file(), and manifest_hash() from Pattern 1.


def verify_manifest(asset_dir: str) -> tuple[bool, list[str]]:
    """Verify current files against INTEGRITY.json."""
    root = Path(asset_dir).resolve()
    manifest_path = root / "INTEGRITY.json"

    if not manifest_path.exists():
        return False, ["INTEGRITY.json not found"]

    manifest = json.loads(manifest_path.read_text())
    if manifest.get("algorithm") != "sha256":
        return False, ["INVALID: unsupported or missing algorithm"]

    recorded = manifest.get("files", {})
    errors = []

    for rel_path, expected_hash in recorded.items():
        current_path = root / rel_path
        if not current_path.exists():
            errors.append(f"MISSING: {rel_path}")
            continue
        actual = hash_file(current_path)
        if actual != expected_hash:
            errors.append(f"MODIFIED: {rel_path}")

    current = generate_manifest(asset_dir, asset_type=manifest.get("asset_type", "agent-asset"))
    for rel_path in current["files"]:
        if rel_path not in recorded:
            errors.append(f"UNTRACKED: {rel_path}")

    expected_manifest_hash = manifest_hash(recorded)
    if manifest.get("manifest_hash") != expected_manifest_hash:
        errors.append("INVALID: manifest_hash does not match recorded files")

    if manifest.get("file_count") != len(recorded):
        errors.append("INVALID: file_count does not match recorded files")

    return not errors, errors


passed, errors = verify_manifest("my-agent-tool")
if passed:
    print("VERIFIED: All files match manifest")
else:
    print(f"FAILED: {len(errors)} issue(s)")
    for e in errors:
    Check that agent dependencies use pinned versions or lockfiles. Treat this as a review aid; package-manager-specific policies may require additional checks.
```

    import json
**Output on tampered plugin:**
    from pathlib import Path


    RANGE_PREFIXES = ("^", "~", ">", "<", "<=", ">=", "*")

```
    def audit_versions(config_path: str) -> list[dict[str, str]]:
  MODIFIED: skills/search/SKILL.md
  MISSING: agency.json
  UNTRACKED: backdoor.py
```

---

## Pattern 3: Dependency Version Audit

                    if ver == "latest" or ver.startswith(RANGE_PREFIXES):

```python
import re

                            "fix": f'Pin to an exact version or commit lockfile: "{pkg}": "{ver.lstrip("^~<>=")}"'
    """Audit dependency version pinning in a config file."""
    findings = []
    path = Path(config_path)
    content = path.read_text()

                if not line or line.startswith("#"):
                    continue
                if ">=" in line and "<" not in line:
        data = json.loads(content)
        for section in ("dependencies", "devDependencies"):
            for pkg, ver in data.get(section, {}).items():
                if ver.startswith("^") or ver.startswith("~") or ver == "*" or ver == "latest":
                        "fix": f"Add an upper bound or pin exactly according to project policy: {line},<next_major"
                        "package": pkg,
                elif re.match(r"^[A-Za-z0-9_.-]+$", line):
                    findings.append({
                        "package": line,
                        "version": "unbounded",
                        "severity": "HIGH",
                        "fix": f"Pin or constrain the package: {line}==[TODO]"
                    })
                        "version": ver,
                        "severity": "HIGH" if ver in ("*", "latest") else "MEDIUM",
                        "fix": f'Pin to exact: "{pkg}": "{ver.lstrip("^~")}"'

    Also check for expected lockfiles such as `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `uv.lock`, `poetry.lock`, `Pipfile.lock`, `go.sum`, `Cargo.lock`, or equivalent project policy files.
                    })

    elif path.name in ("requirements.txt", "pyproject.toml"):
        for line in content.splitlines():
            line = line.strip()
    Use integrity verification and dependency review as a gate before promotion.
                findings.append({
                    "package": line.split(">=")[0].strip(),
    import json
    from pathlib import Path


    # Requires: verify_manifest() and audit_versions() from earlier patterns.


    def promotion_check(asset_dir: str) -> dict:
        """Check whether an agent asset is ready for promotion."""
        root = Path(asset_dir).resolve()
                    "fix": f"Add upper bound: {line},<next_major"
                })
        passed, errors = verify_manifest(asset_dir)
```

---

## Pattern 4: Promotion Gate
        required_files = ["README.md"]
        missing = [relative for relative in required_files if not (root / relative).exists()]
        "errors": errors
    }
            "passed": not missing,
    # 2. Required files exist
    root = Path(plugin_dir)
    required = ["README.md"]
        dependency_files = [
            root / "package.json",
            root / "requirements.txt",
            root / "pyproject.toml",
        ]
        findings = []
        for dependency_file in dependency_files:
            if dependency_file.exists():
                findings.extend(audit_versions(str(dependency_file)))

        mcp_config = root / ".mcp.json"
        if mcp_config.exists():
            config = json.loads(mcp_config.read_text())
            for server_name, server in config.get("mcpServers", {}).items():
                for arg in server.get("args", []) if isinstance(server, dict) else []:
                    if isinstance(arg, str) and ("@latest" in arg or arg.endswith(":latest")):
                        findings.append({
                            "package": server_name,
                            "version": arg,
                            "severity": "HIGH",
                            "fix": "Replace latest with a reviewed exact version."
                        })

        checks["dependency_pinning"] = {
            "passed": not findings,
            "findings": findings
        }
    checks["required_files"] = {
        return {
            "ready": all(check["passed"] for check in checks.values()),
            "checks": checks,
        }
        unpinned = []

    result = promotion_check("my-agent-tool")
            if isinstance(server, dict):
                for arg in server.get("args", []):
                    if isinstance(arg, str) and "@latest" in arg:
        print("Agent asset NOT ready:")
        checks["pinned_deps"] = {
            "passed": len(unpinned) == 0,
            "unpinned": unpinned
        }

    # Overall
    all_passed = all(c["passed"] for c in checks.values())
    return {"ready": all_passed, "checks": checks}

result = promotion_check("my-plugin/")
if result["ready"]:
    print("Plugin is ready for production promotion")
else:
    print("Plugin NOT ready:")
    for name, check in result["checks"].items():
        if not check["passed"]:
            print(f"  FAILED: {name}")
```

---

## CI Integration

Add to your GitHub Actions workflow:

```yaml
- name: Verify agent asset integrity
  run: |
    ASSET_DIR="${{ matrix.asset || '.' }}"
    cd "$ASSET_DIR"
    python <<'PY'
    from pathlib import Path
    import json, hashlib, sys

    EXCLUDE_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', 'dist', 'build'}
    EXCLUDE_FILES = {'INTEGRITY.json', '.DS_Store'}

    def hash_file(path):
        digest = hashlib.sha256()
        with open(path, 'rb') as handle:
            for chunk in iter(lambda: handle.read(8192), b''):
                digest.update(chunk)
        return digest.hexdigest()

    def current_files():
        files = {}
        for path in sorted(Path('.').rglob('*')):
            if not path.is_file() or path.name in EXCLUDE_FILES:
                continue
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            files[path.as_posix()] = hash_file(path)
        return files

    def manifest_hash(files):
        digest = hashlib.sha256()
        for relative_path, file_hash in sorted(files.items()):
            digest.update(relative_path.encode('utf-8'))
            digest.update(b'\0')
            digest.update(file_hash.encode('ascii'))
            digest.update(b'\n')
        return digest.hexdigest()

    manifest = json.loads(Path('INTEGRITY.json').read_text())
    recorded = manifest.get('files', {})
    current = current_files()
    errors = []

    if manifest.get('algorithm') != 'sha256':
        errors.append('INVALID: unsupported or missing algorithm')
    if manifest.get('manifest_hash') != manifest_hash(recorded):
        errors.append('INVALID: manifest_hash does not match recorded files')

    for rel, expected in recorded.items():
        path = Path(rel)
        if not path.exists():
            errors.append(f'MISSING: {rel}')
        elif hash_file(path) != expected:
            errors.append(f'MODIFIED: {rel}')

    for rel in current:
        if rel not in recorded:
            errors.append(f'UNTRACKED: {rel}')

    if errors:
        for error in errors:
            print(f'::error::{error}')
        sys.exit(1)

    print(f'Verified {len(recorded)} files')
    PY
```

---

## Review Checklist

| Practice | Rationale |
|----------|-----------|
| Generate the manifest after review-ready changes | Ensures the manifest represents what reviewers approved |
| Commit the manifest with the asset | Gives CI and reviewers a stable verification target |
| Verify before deployment or publication | Catches post-review modifications and untracked additions |
| Bind paths into the manifest hash | Detects path swaps as well as file-content changes |
| Exclude generated and local-only files | Keeps manifests stable and avoids recording secrets or caches |
| Pin dependencies or commit lockfiles | Reduces install-time drift and review ambiguity |
| Record provenance notes | Preserve source, version, reviewer, and release evidence where policy requires it |

## Finding Severity

| Finding | Default Severity | Action |
|---------|------------------|--------|
| Missing `INTEGRITY.json` | High | Generate and review a manifest before promotion |
| Modified recorded file | High | Re-review the change and regenerate the manifest if approved |
| Untracked executable or configuration file | High | Review and add it to the manifest, or exclude it with justification |
| Invalid `manifest_hash` or `file_count` | High | Treat the manifest as tampered or malformed |
| Unpinned dependency or `latest` tag | Medium to High | Pin exactly or add an approved lockfile |
| Missing provenance evidence | Medium | Add source, reviewer, version, and release notes, or mark `[TODO]` |
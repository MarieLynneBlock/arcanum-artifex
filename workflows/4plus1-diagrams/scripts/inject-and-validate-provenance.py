#!/usr/bin/env python3
"""Inject the canonical-source-ref provenance cell into workflow draw.io templates
and validate each template with the bundled draw.io validator.

Idempotent: templates that already contain the provenance cell are skipped.

All paths are resolved relative to this script's location, so the bundle remains
standalone and copyable.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates" / "drawio"
VALIDATOR = ROOT / "skills" / "draw-io-diagram-generator" / "scripts" / "validate-drawio.py"

PROVENANCE_CELL = (
    '        <mxCell id="canonical-source-ref" '
    'value="canonical-source-path=&lt;path&gt;&#10;'
    'canonical-source-format=&lt;mmd|puml&gt;&#10;'
    'canonical-source-summary=&lt;short summary&gt;" '
    'style="text;strokeColor=none;fillColor=none;opacity=0;html=1;" '
    'vertex="1" parent="1">\n'
    '          <mxGeometry x="0" y="0" width="1" height="1" as="geometry" />\n'
    '        </mxCell>\n'
)


def main() -> int:
    for f in sorted(TEMPLATES_DIR.glob("*.drawio")):
        s = f.read_text()
        if 'id="canonical-source-ref"' in s:
            print(f"SKIP {f.name} (already has provenance)")
            continue
        new = re.sub(
            r"(?P<i>[ \t]*)</root>",
            lambda m: PROVENANCE_CELL + m.group("i") + "</root>",
            s,
            count=1,
        )
        if new == s:
            print(f"NO MATCH {f.name}")
            return 2
        f.write_text(new)
        print(f"INJECTED {f.name}")

    print("--- validate ---")
    fail = 0
    for f in sorted(TEMPLATES_DIR.glob("*.drawio")):
        r = subprocess.run(
            [sys.executable, str(VALIDATOR), str(f), "--require-provenance"],
            capture_output=True,
            text=True,
        )
        print(f.name, "->", "OK" if r.returncode == 0 else "FAIL")
        if r.returncode != 0:
            print(r.stdout)
            print(r.stderr)
            fail += 1
    return fail


if __name__ == "__main__":
    sys.exit(main())

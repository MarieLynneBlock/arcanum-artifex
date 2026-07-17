"""Check deck text, slide count, and notes-slide count without external packages."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from zipfile import ZipFile


SLIDE_PATTERN = re.compile(r"ppt/slides/slide\d+\.xml$")
NOTES_PATTERN = re.compile(r"ppt/notesSlides/notesSlide\d+\.xml$")
TEXT_PATTERN = re.compile(r"<a:t>(.*?)</a:t>")
DISALLOWED_PATTERNS = ("—", "TODO", "lorem", "xxx", "[insert")


def extract_text(archive: ZipFile, name: str) -> str:
    xml = archive.read(name).decode("utf-8", errors="ignore")
    return "\n".join(html.unescape(value) for value in TEXT_PATTERN.findall(xml))


def main() -> int:
    pptx = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist/deck.pptx")
    if not pptx.is_file():
        print(f"PPTX not found: {pptx}", file=sys.stderr)
        return 2

    with ZipFile(pptx) as archive:
        slide_files = sorted(name for name in archive.namelist() if SLIDE_PATTERN.match(name))
        notes_files = sorted(name for name in archive.namelist() if NOTES_PATTERN.match(name))
        print(f"slides={len(slide_files)} notes={len(notes_files)}")

        matches: list[tuple[str, str]] = []
        for name in [*slide_files, *notes_files]:
            text = extract_text(archive, name).lower()
            for pattern in DISALLOWED_PATTERNS:
                if pattern.lower() in text:
                    matches.append((name, pattern))

    print(f"bad_matches={len(matches)}")
    for name, pattern in matches:
        print(f"{name}: {pattern}")
    return 1 if matches else 0


if __name__ == "__main__":
    raise SystemExit(main())
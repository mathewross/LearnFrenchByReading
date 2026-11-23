#!/usr/bin/env python3
"""Fail if the size budgets are exceeded: app shell < 100 KB gzipped, each story <= 60 KB,
whole library < 3 MB. Run after tools/build.py."""
import gzip
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
SHELL_GZ_BUDGET = 100 * 1024
STORY_BUDGET = 40 * 1024  # gzipped: what GitHub Pages actually sends
LIBRARY_BUDGET = 3 * 1024 * 1024


def gz(p):
    return len(gzip.compress(p.read_bytes(), 9))


def main():
    problems = []
    shell = [DOCS / "index.html", DOCS / "sw.js", DOCS / "manifest.webmanifest", *sorted((DOCS / "css").glob("*.css")), *sorted((DOCS / "js").glob("*.js"))]
    shell_gz = sum(gz(p) for p in shell if p.exists())
    print(f"app shell: {shell_gz / 1024:.1f} KB gzipped (budget {SHELL_GZ_BUDGET // 1024} KB)")
    if shell_gz > SHELL_GZ_BUDGET:
        problems.append("app shell over budget")
    total = 0
    for p in sorted((DOCS / "data" / "stories").glob("*.json")):
        total += p.stat().st_size
        size = gz(p)
        if size > STORY_BUDGET:
            problems.append(f"{p.name}: {size / 1024:.1f} KB gzipped > {STORY_BUDGET // 1024} KB")
    for p in (DOCS / "data").glob("*.json"):
        total += p.stat().st_size
    icons = sum(p.stat().st_size for p in (DOCS / "icons").glob("*.png"))
    imgs = sum(p.stat().st_size for p in (DOCS / "img").glob("*.svg")) if (DOCS / "img").exists() else 0
    total += icons + imgs
    print(f"story pictures: {imgs / 1024:.1f} KB")
    print(f"library + data + icons: {total / 1024:.1f} KB (budget {LIBRARY_BUDGET // 1024} KB)")
    if total > LIBRARY_BUDGET:
        problems.append("library over budget")
    if problems:
        print("BUDGET CHECK FAILED:\n  - " + "\n  - ".join(problems))
        return 1
    print("budgets OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

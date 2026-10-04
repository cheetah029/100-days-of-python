#!/usr/bin/env python3
"""Build data/manifest.json and data/<slug>.json for the static site.

Reads the full slug list from ~/workspace/replit-projects/slugs.txt and the
checked-out projects under ~/workspace/100-days-of-python/projects/<slug>/.
Slugs with no local project directory are skipped (more projects arrive later;
just re-run this script).

Outputs (under ~/workspace/100-days-of-python/docs/):
  data/manifest.json      - [{slug, title, type, files, entry}, ...]
  data/<slug>.json        - {slug, files: {filename: content}} (text files only)
"""

import json
import os
import re
import sys

HOME = os.path.expanduser("~")
REPO = os.path.join(HOME, "workspace", "100-days-of-python")
PROJECTS_DIR = os.path.join(REPO, "projects")
SLUGS_FILE = os.path.join(HOME, "workspace", "replit-projects", "slugs.txt")
DOCS_DIR = os.path.join(REPO, "docs")
DATA_DIR = os.path.join(DOCS_DIR, "data")

TURTLE_SLUGS = {
    "snake-game",
    "pong-game",
    "turtle-crossing-start",
    "turtle-race-start",
    "etch-a-sketch-start",
    "hirst_painting-start",
    "us-states-game-start",
}

TKINTER_SLUGS = {
    "mile-to-kilo-converter",
    "tkinter-widget-demo",
    "pomodoro-start",
    "flash-card-project-start",
    "quizzler-app-start",
    "kanye-quotes-start",
    "password-manager-start",
}

# Junk we never want in the site data.
SKIP_NAMES = {
    ".replit",
    ".replit.backup",
    "replit.nix",
    "poetry.lock",
}
SKIP_SUFFIXES = (".pyc", ".pyo")
SKIP_DIRS = {"__pycache__", ".git", ".venv", "venv", "node_modules"}


def project_type(slug: str) -> str:
    if slug in TURTLE_SLUGS:
        return "turtle"
    if slug in TKINTER_SLUGS:
        return "tkinter"
    return "console"


def humanize(slug: str) -> str:
    """day-2-3-exercise -> 'Day 2-3 Exercise'; Day-7-Hangman-5-Start -> 'Day 7 Hangman 5 Start'."""
    parts = re.split(r"[-_]", slug)
    merged = []
    for p in parts:
        if not p:
            continue
        if merged and merged[-1].isdigit() and p.isdigit():
            merged[-1] = merged[-1] + "-" + p
        else:
            merged.append(p.capitalize() if p.isalpha() else p)
    return " ".join(merged)


def is_text_file(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(8192)
        if b"\x00" in chunk:
            return False
        chunk.decode("utf-8")
        return True
    except (OSError, UnicodeDecodeError):
        return False


def collect_files(proj_dir: str):
    """Return {relative_filename: content} for all wanted text files."""
    collected = {}
    for root, dirs, files in os.walk(proj_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in sorted(files):
            if name in SKIP_NAMES or name.endswith(SKIP_SUFFIXES):
                continue
            if name.startswith("pyproject.toml"):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, proj_dir)
            if not is_text_file(full):
                continue
            try:
                with open(full, "r", encoding="utf-8") as f:
                    collected[rel] = f.read()
            except OSError:
                continue
    return collected


def main() -> int:
    with open(SLUGS_FILE, "r", encoding="utf-8") as f:
        slugs = [line.strip() for line in f if line.strip()]

    os.makedirs(DATA_DIR, exist_ok=True)

    manifest = []
    present = 0
    for slug in slugs:
        proj_dir = os.path.join(PROJECTS_DIR, slug)
        if not os.path.isdir(proj_dir):
            continue  # not downloaded yet; skip silently
        files = collect_files(proj_dir)
        if not files:
            continue
        entry = "main.py" if "main.py" in files else next(
            (n for n in files if n.endswith(".py")), ""
        )
        manifest.append(
            {
                "slug": slug,
                "title": humanize(slug),
                "type": project_type(slug),
                "files": sorted(files.keys()),
                "entry": entry,
            }
        )
        with open(os.path.join(DATA_DIR, slug + ".json"), "w", encoding="utf-8") as f:
            json.dump({"slug": slug, "files": files}, f, ensure_ascii=False)
        present += 1

    with open(os.path.join(DATA_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"slugs total: {len(slugs)}, projects present: {present}")
    print(f"wrote {os.path.join(DATA_DIR, 'manifest.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

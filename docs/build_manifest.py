"""Build data/manifest.json and data/<slug>.json for the static site.

Run from anywhere:  python3 docs/build_manifest.py

All paths are relative to this script's own location (the repo root is the
parent of docs/), so it works from any clone. Every directory under
projects/ is a project; no external slug list is needed. Re-run it whenever
projects are added or changed.

Per project:
  * Nested duplicate folders (projects/<slug>/<slug>/main.py) are handled: if
    the top level has a main.py, nested copies that also have a main.py are
    ignored; if the top level has none and exactly one subfolder has one, that
    subfolder is treated as the project root (so imports/data files resolve).
  * Junk (poetry.lock, pyproject.toml*, Replit backups like *.~1~, nohup.out,
    binary files, very large files) is left out.
  * type is "turtle" / "tkinter" / "console", from the override sets below plus
    auto-detection of `import turtle` / `import tkinter` in the sources.
    tkinter projects get "app": true only if docs/apps/<slug>/index.html exists.

Outputs (under docs/):
  data/manifest.json      - [{slug, title, type, files, entry[, app]}, ...]
  data/<slug>.json        - {slug, files: {filename: content}} (text files only)
"""

import json
import os
import re
import sys

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(DOCS_DIR)
PROJECTS_DIR = os.path.join(REPO, "projects")
DATA_DIR = os.path.join(DOCS_DIR, "data")
APPS_DIR = os.path.join(DOCS_DIR, "apps")

# Explicit overrides; anything not listed is auto-detected from its imports
# (so new turtle / tkinter projects are picked up even if not listed here).
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
    ".replit.nix",
    "poetry.lock",
    "nohup.out",
    ".DS_Store",
    "Thumbs.db",
}
SKIP_SUFFIXES = (".pyc", ".pyo", ".log")
SKIP_PREFIXES = ("pyproject.toml", "Pipfile")
BACKUP_RE = re.compile(r"\.~\d*~$|~$")  # Replit/editor backups: foo.~1~, foo~
SKIP_DIRS = {
    "__pycache__", ".git", ".venv", "venv", "node_modules",
    ".cache", ".local", ".upm", ".config", ".pythonlibs", ".idea", ".vscode",
}
MAX_FILE_BYTES = 512 * 1024

IMPORT_TMPL = r"^\s*(?:import|from)\s+%s\b"


def project_type(slug: str, files: dict) -> str:
    src = "\n".join(c for n, c in files.items() if n.endswith(".py"))
    has_tk = re.search(IMPORT_TMPL % "(?:tkinter|Tkinter)", src, re.M)
    has_turtle = re.search(IMPORT_TMPL % "turtle", src, re.M)
    if slug in TKINTER_SLUGS or has_tk:
        return "tkinter"
    if slug in TURTLE_SLUGS or has_turtle:
        return "turtle"
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
        elif p.isalpha():
            merged.append(p if (p.isupper() and len(p) > 1) else p.capitalize())
        else:
            merged.append(p)
    return " ".join(merged)


def is_wanted_name(name: str) -> bool:
    return not (
        name in SKIP_NAMES
        or name.endswith(SKIP_SUFFIXES)
        or name.startswith(SKIP_PREFIXES)
        or BACKUP_RE.search(name)
    )


def read_text(path: str):
    """Return file text, or None if binary / unreadable / too large."""
    try:
        if os.path.getsize(path) > MAX_FILE_BYTES:
            return None
        with open(path, "rb") as f:
            data = f.read()
        if b"\x00" in data[:8192]:
            return None
        return data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def subdirs(path: str):
    return sorted(
        d for d in os.listdir(path)
        if d not in SKIP_DIRS and os.path.isdir(os.path.join(path, d))
    )


def walk_files(root: str, exclude=()):
    """Yield (relative_name, full_path), skipping SKIP_DIRS and excluded top-level dirs."""
    for cur, dirs, files in os.walk(root):
        dirs[:] = sorted(
            d for d in dirs
            if d not in SKIP_DIRS and not (cur == root and d in exclude)
        )
        for name in sorted(files):
            if is_wanted_name(name):
                full = os.path.join(cur, name)
                yield os.path.relpath(full, root).replace(os.sep, "/"), full


def collect_files(proj_dir: str, warn=None):
    """Return {relative_filename: content} for all wanted text files.

    Handles nested duplicate folders (see module docstring).
    """
    nested = [d for d in subdirs(proj_dir)
              if os.path.isfile(os.path.join(proj_dir, d, "main.py"))]
    exclude, hoist = (), None
    if os.path.isfile(os.path.join(proj_dir, "main.py")):
        exclude = tuple(nested)           # nested copies of the same project
    elif len(nested) == 1:
        hoist = nested[0]                 # the real project lives one level down
        exclude = (hoist,)

    collected = {}
    sources = list(walk_files(proj_dir, exclude))
    if hoist:
        sources += list(walk_files(os.path.join(proj_dir, hoist)))  # overrides
    for rel, full in sources:
        text = read_text(full)
        if text is None:
            if warn:
                warn(f"skipped non-text/large file: {rel}")
            continue
        collected[rel] = text
    return dict(sorted(collected.items()))


def pick_entry(files: dict) -> str:
    if "main.py" in files:
        return "main.py"
    pys = sorted((n for n in files if n.endswith(".py")),
                 key=lambda n: (n.count("/"), n))
    return pys[0] if pys else ""


def write_if_changed(path: str, text: str) -> None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            if f.read() == text:
                return
    except OSError:
        pass
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main() -> int:
    if not os.path.isdir(PROJECTS_DIR):
        print(f"error: projects directory not found: {PROJECTS_DIR}", file=sys.stderr)
        return 1
    os.makedirs(DATA_DIR, exist_ok=True)

    slugs = sorted(
        (d for d in os.listdir(PROJECTS_DIR)
         if not d.startswith(".") and os.path.isdir(os.path.join(PROJECTS_DIR, d))),
        key=lambda d: (d.lower(), d),
    )

    manifest = []
    for slug in slugs:
        files = collect_files(
            os.path.join(PROJECTS_DIR, slug),
            warn=lambda m, s=slug: print(f"  [{s}] {m}"),
        )
        if not files:
            print(f"  [{slug}] no usable files, skipped")
            continue
        entry = pick_entry(files)
        ptype = project_type(slug, files)
        item = {
            "slug": slug,
            "title": humanize(slug),
            "type": ptype,
            "files": sorted(files.keys()),
            "entry": entry,
        }
        if ptype == "tkinter":
            item["app"] = os.path.isfile(os.path.join(APPS_DIR, slug, "index.html"))
            if not item["app"]:
                print(f"  [{slug}] tkinter project has no docs/apps/{slug}/index.html yet")
        elif not entry:
            print(f"  [{slug}] warning: no .py file to run")
        manifest.append(item)
        write_if_changed(
            os.path.join(DATA_DIR, slug + ".json"),
            json.dumps({"slug": slug, "files": files}, ensure_ascii=False),
        )

    write_if_changed(
        os.path.join(DATA_DIR, "manifest.json"),
        json.dumps(manifest, indent=2, ensure_ascii=False),
    )

    known = {m["slug"] for m in manifest} | {"manifest"}
    for name in sorted(os.listdir(DATA_DIR)):
        if name.endswith(".json") and name[:-5] not in known:
            print(f"  warning: orphan data file (no project): data/{name}")

    print(f"projects found: {len(slugs)}, in manifest: {len(manifest)}")
    print(f"wrote {os.path.join(DATA_DIR, 'manifest.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

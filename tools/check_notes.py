"""
Lint the notes:
  * front matter has title, summary, tags, level, time
  * every relative markdown link and image points to an existing file
  * no em dashes or en dashes anywhere in the repo's text files (style rule)
Exit code 1 on any problem, so it can run in CI.
"""

import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
REQUIRED = ("title", "summary", "tags", "level", "time")
BANNED = {chr(0x2014): "em dash", chr(0x2013): "en dash"}
TEXT_EXT = (".md", ".py", ".html", ".js", ".css", ".json", ".yml", ".yaml", ".txt")


def front_matter(text):
    if not text.startswith("---\n"):
        return None
    end = text.index("\n---\n", 4)
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def main():
    problems = []
    notes = sorted(glob.glob(os.path.join(ROOT, "notes", "**", "*.md"), recursive=True))
    for path in notes:
        rel = os.path.relpath(path, ROOT)
        text = open(path).read()
        meta = front_matter(text)
        if meta is None:
            problems.append("%s: missing front matter" % rel)
            continue
        for key in REQUIRED:
            if not meta.get(key):
                problems.append("%s: front matter missing '%s'" % (rel, key))
        if " - " in meta.get("summary", ""):
            problems.append("%s: summary uses ' - ' as a separator (use a colon, commas or parentheses)" % rel)
        if "> **TL;DR**" not in text:
            problems.append("%s: missing the '> **TL;DR**' box under the title" % rel)
        body = re.sub(r"```.*?```", "", text, flags=re.S)       # ignore code blocks
        for target in LINK.findall(body):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            file_part = target.split("#")[0]
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), file_part))):
                problems.append("%s: broken link -> %s" % (rel, target))

    for path in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
        if not path.endswith(TEXT_EXT) or "/.git/" in path or "/node_modules/" in path:
            continue
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for ch, name in BANNED.items():
            if ch in text:
                line = text[: text.index(ch)].count("\n") + 1
                problems.append("%s:%d: contains an %s" % (os.path.relpath(path, ROOT), line, name))

    for p in problems:
        print(p)
    print("checked %d notes, %d problem(s)" % (len(notes), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

"""
Embed runnable code from builds/*.py into the notes so code and notes never drift.

In any note, write:

    <!-- code: builds/lru_cache.py -->
    <!-- /code -->

and run `python3 tools/sync_builds.py`. Everything between the markers is replaced
with a fenced python block containing the current file contents.
"""

import glob
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PATTERN = re.compile(r"(<!-- code: (?P<path>[^ ]+) -->\n)(?P<body>.*?)(<!-- /code -->)", re.S)


def sync():
    changed = 0
    for note in glob.glob(os.path.join(ROOT, "notes", "**", "*.md"), recursive=True):
        text = open(note).read()

        def repl(m):
            src = open(os.path.join(ROOT, m.group("path"))).read().rstrip("\n")
            return "%s```python\n%s\n```\n%s" % (m.group(1), src, m.group(4))

        new = PATTERN.sub(repl, text)
        if new != text:
            open(note, "w").write(new)
            changed += 1
    print("synced code blocks in %d note(s)" % changed)


if __name__ == "__main__":
    sync()

"""
Render every diagram defined in tools/diagrams/defs/*.py.

Usage:
    python3 tools/diagrams/build.py            # render all diagrams
    python3 tools/diagrams/build.py caching    # only diagrams whose name contains "caching"

Each defs module exposes build() which returns a list of sketch.Diagram objects.
Outputs:
    assets/diagrams/<name>.svg                     embedded in the notes
    assets/diagrams/excalidraw/<name>.excalidraw   open in excalidraw.com to edit
"""

import importlib
import os
import pkgutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "assets", "diagrams")

sys.path.insert(0, HERE)


def all_diagrams():
    import defs
    diagrams = []
    for m in sorted(pkgutil.iter_modules(defs.__path__), key=lambda m: m.name):
        mod = importlib.import_module("defs." + m.name)
        diagrams.extend(mod.build())
    names = [d.name for d in diagrams]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise SystemExit("duplicate diagram names: %s" % ", ".join(sorted(dupes)))
    return diagrams


def main(argv):
    filt = argv[1] if len(argv) > 1 else ""
    count = 0
    for d in all_diagrams():
        if filt in d.name:
            d.save(OUT)
            count += 1
    print("rendered %d diagram(s) into %s" % (count, os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main(sys.argv)

"""Every "deck slides 20–21" in a notebook must point at slides that exist.

    python3 tools/audit_pointers.py

The decks were rebuilt several times; the notebooks were not. Eleven of thirteen ended up
pointing past the end of their own deck -- session 10 sent readers to slide 37 of a
19-slide deck. This check makes that impossible to miss again.
"""
import glob, json, os, re, sys


def pointer_lines(md):
    for l in md.splitlines():
        s = l.lstrip()
        if "deck slide" in s.lower() or (s.startswith("|") and "·" in s):
            yield s


def main():
    bad = []
    for nbf in sorted(glob.glob("*/*_tutorial.ipynb")):
        folder = os.path.dirname(nbf)
        n = open(glob.glob(folder + "/*_slides.html")[0]).read().count("<section")
        md = "\n".join("".join(c["source"]) for c in json.load(open(nbf))["cells"]
                       if c["cell_type"] == "markdown")
        refs = set()
        for l in pointer_lines(md):
            for a, b in re.findall(r"(\d{1,2})\s*[–\-—]\s*(\d{1,2})", l):
                refs |= {int(a), int(b)}
            refs |= {int(m) for m in re.findall(r"deck slides?\s+(\d{1,2})\b", l, re.I)}
            cells = l.strip().strip("|").split("|")
            if len(cells) > 1 and cells[1].strip().isdigit():
                refs.add(int(cells[1].strip()))
        over = sorted(r for r in refs if r > n)
        print(f"  {'BAD' if over else 'ok '} {folder:28} deck has {n:3} slides"
              + (f"   POINTS AT {over}" if over else ""))
        if over: bad.append(folder)
    print("\n" + ("every pointer lands inside its deck" if not bad else f"{len(bad)} notebook(s) wrong"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

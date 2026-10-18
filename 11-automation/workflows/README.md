# The workflow from session 11

`validate.yml` is the CI job the session builds. It checks that every deck in this repository is
balanced and carries its own pictures, that no notebook ships stored error outputs, that the course
index links every built session, and that the example written by the notebook is still the file
GitHub runs.

Run locally over the whole repo it passes across **13 decks and 12 notebooks**.

## It is live

The same file is committed as `.github/workflows/validate.yml`, so it runs on every push and every
pull request; `gh run list` shows the runs.

Getting it there took one extra step. GitHub refuses a push that creates or changes a workflow file
unless the token carries the `workflow` scope:

```
! [remote rejected] main -> main (refusing to allow an OAuth App to create or
  update workflow `.github/workflows/validate.yml` without `workflow` scope)
```

```bash
gh auth refresh -s workflow          # grant the scope, once
```

Three copies have to stay identical: the `%%writefile ci-example.yml` cell in
`automation_tutorial.ipynb` (what the session teaches), this file, and `.github/workflows/validate.yml`
(what GitHub runs). The workflow's last step compares the first against the third, so drift fails CI
instead of going unnoticed.

## Running the same checks now, without GitHub

```bash
python3 - <<'CHECK'
import glob, json, os, re, sys
bad = []
for f in glob.glob("*/*_slides.html"):
    t = open(f).read()
    if t.count("<section") != t.count("</section>"): bad.append(f + ": unbalanced")
    # src, not href: the pictures must be embedded, the reading list may link out
    ext = re.findall(r'src="(?!#|data:)[^"]+"', t)
    if ext: bad.append(f"{f}: external {ext[:2]}")
for f in glob.glob("*/*_tutorial.ipynb"):
    nb = json.load(open(f))
    errs = [o for c in nb["cells"] for o in c.get("outputs", []) if o.get("output_type") == "error"]
    if errs: bad.append(f"{f}: {len(errs)} stored errors")
readme = open("README.md").read()
bad += [f"{d} not linked in README" for d in sorted(glob.glob("*/"))
        if glob.glob(os.path.join(d, "*_slides.html")) and f"({d.rstrip('/')})" not in readme]
print("FAIL:", *bad, sep="\n  ") if bad else print("PASS")
sys.exit(1 if bad else 0)
CHECK
```

# The workflow from session 11

`validate.yml` is the CI job the session builds. It checks that every deck in this repository is
balanced and has no external references, that no notebook ships stored error outputs, and that the
course index links every built session.

Run locally over the whole repo it passes across **11 decks and 12 notebooks**.

## Activating it

It lives here rather than in `.github/workflows/` because GitHub refuses a push that creates a
workflow file unless the token has the `workflow` scope:

```
! [remote rejected] main -> main (refusing to allow an OAuth App to create or
  update workflow `.github/workflows/validate.yml` without `workflow` scope)
```

To turn it on:

```bash
gh auth refresh -s workflow          # grant the scope, once
mkdir -p .github/workflows
cp 11-automation/workflows/validate.yml .github/workflows/
git add .github/workflows/validate.yml
git commit -m "ci: validate decks and notebooks on every push"
git push
```

Then it runs on every push and pull request, and `gh run list` will show it.

## Running the same checks now, without GitHub

```bash
python3 - <<'CHECK'
import glob, json, os, re, sys
bad = []
for f in glob.glob("*/*_slides.html"):
    t = open(f).read()
    if t.count("<section") != t.count("</section>"): bad.append(f + ": unbalanced")
    ext = re.findall(r'(?:src|href)="(?!#|data:)[^"]+"', t)
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

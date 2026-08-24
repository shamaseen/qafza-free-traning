"""Execute a notebook and prove it actually worked.

    python3 tools/verify.py <notebook> [timeout] [--claim "text that must appear"]...

Checks, in order:
  1. every code cell ran (has an execution_count)
  2. zero Python exceptions
  3. zero FAILING SHELL COMMANDS -- `!cmd` errors never raise in Jupyter, so a broken
     build or a rejected config looks like success unless you read the output. Two real
     bugs in this course hid exactly there.
  4. every --claim string appears somewhere in the output, so the notebook's headline
     demonstration is proved rather than assumed.
Exit code 0 only if all pass.
"""
import json, re, subprocess, sys, tempfile, os

FAIL = re.compile(r"(validation failed|^ERROR:|\bERROR\b:|fatal:|Traceback \(most recent"
                  r"|command not found|No such file or directory|nothing to commit"
                  r"|error: |failed to |cannot )", re.I | re.M)
IGNORE = re.compile(r"tokenizers|dependency resolver|pip version|Experiment with name"
                    r"|WARNING|warn|numexpr|bottleneck|Downloading|already exists"
                    r"|deprecat|InsecureRequest"
                    # Ray logs this from the raylet while the Serve controller is torn
                    # down. It is internal retry noise, not a failure of the notebook --
                    # the only named exception in this list, kept narrow on purpose.
                    r"|ServeController\.graceful_shutdown", re.I)


def outputs_text(cell):
    t = ""
    for o in cell.get("outputs", []):
        t += "".join(o.get("text", []))
        d = o.get("data", {})
        t += "".join(d.get("text/plain", []))
    return t


def main():
    nb_path = sys.argv[1]
    timeout = next((a for a in sys.argv[2:] if a.isdigit()), "900")
    claims = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--claim"]

    out = os.path.join(tempfile.mkdtemp(), "out.ipynb")
    cmd = ["jupyter", "nbconvert", "--to", "notebook", "--execute", nb_path,
           "--output", out, f"--ExecutePreprocessor.timeout={timeout}", "--allow-errors"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(out):
        print("FAIL: nbconvert produced nothing\n", r.stderr[-1500:]); return 1

    nb = json.load(open(out))
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    notrun = [i for i, c in enumerate(nb["cells"])
              if c["cell_type"] == "code" and c.get("execution_count") is None]
    errs = [(i, "".join(c["source"]).splitlines()[0][:60], o["ename"], o["evalue"][:140])
            for i, c in enumerate(nb["cells"]) for o in c.get("outputs", [])
            if o.get("output_type") == "error"]
    alltext = "\n".join(outputs_text(c) for c in nb["cells"])
    shell = [l.strip()[:110] for l in alltext.splitlines()
             if FAIL.search(l) and not IGNORE.search(l)]
    missing = [c for c in claims if c not in alltext]

    print(f"{nb_path}")
    print(f"  cells            {len(nb['cells'])} ({len(code)} code)")
    print(f"  executed         {len(code) - len(notrun)}/{len(code)}")
    print(f"  exceptions       {len(errs)}")
    for e in errs: print("     ", e)
    print(f"  shell failures   {len(shell)}")
    for s in shell: print("      !", s)
    print(f"  claims proved    {len(claims) - len(missing)}/{len(claims)}")
    for m in missing: print("      MISSING:", m)

    ok = not notrun and not errs and not shell and not missing
    print("  ->", "PASS" if ok else "FAIL")
    print(f"  executed copy: {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

"""Every number a deck shows as program output must be real.

    python3 tools/audit_decks.py

A slide that quotes output is making a claim about what happened on a machine. This
walks each deck's `<span class="o">` blocks -- the ones styled as program output -- and
checks their numbers and hashes against that session's notebook. It caught six decks
quoting figures the notebook never printed, and one quoting a run id from an earlier run.

Generic illustrations of what a command prints are legitimate teaching material, so they
are listed below with a reason. Anything not on that list has to be real.
"""
import glob, html, json, os, re, sys

# text, why it is not a measurement. Keep this list short and argued.
ALLOWED = {
    "array([0.83, 0.85, 0.81, 0.86, 0.84])": "crash course: the shape of a cross_val_score result",
    "cv accuracy: 0.94":                     "a hypothetical good-looking score, in a comparison card",
    "INFO:     Uvicorn running on http://127.0.0.1:8000": "uvicorn's own default, on an install slide",
    "{'CPU': 16.0, 'memory': 1.6e10, 'object_store_memory': 4.7e9}": "shape of ray.cluster_resources()",
    "a1b2c3d data: customers export 2026-01": "an invented commit, in a git crash course",
    "Listening at: http://127.0.0.1:5000":   "mlflow's own default port, on an install slide",
    '{"predictions": [0.83]}':               "shape of an MLflow REST response",
    "aa0ebaab931a540d9ffe0a40a6563007":      "an example md5, explaining what a hash is",
}


def nb_text(path):
    nb = json.load(open(path))
    return "".join("".join(o.get("text", [])) + "".join(o.get("data", {}).get("text/plain", []))
                   for c in nb["cells"] for o in c.get("outputs", []))


def main():
    problems, checked = [], 0
    for deck in sorted(glob.glob("*/*_slides.html")):
        out = nb_text(glob.glob(os.path.dirname(deck) + "/*_tutorial.ipynb")[0])
        flat = re.sub(r"\s+", " ", out)
        for block in re.findall(r'<span class="o">(.*?)</span>', open(deck).read(), re.S):
            line = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", block))).strip()
            if len(line) < 8 or line in flat:
                continue
            if any(a in line or re.sub(r"\s+", " ", a) in line for a in ALLOWED):
                continue
            checked += 1
            nums = re.findall(r"\d+\.\d+(?:e[-+]?\d+)?|\b\d{2,}\b", line)
            hashes = re.findall(r"\b[0-9a-f]{8,}\b", line)
            missing = [v for v in dict.fromkeys(nums + hashes) if v not in out]
            if missing:
                problems.append(f"{deck}\n    not in the notebook: {missing[:6]}\n    quoted: {line[:96]}")
    print(f"checked {checked} quoted-output blocks in {len(glob.glob('*/*_slides.html'))} decks"
          f" ({len(ALLOWED)} generic illustrations allowed by name)")
    print("\n".join(problems) if problems else "every quoted figure comes from its notebook")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

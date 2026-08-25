"""Run every notebook in the course and check it still proves what it claims.

    python3 tools/verify_all.py            # all of them, in order
    python3 tools/verify_all.py 04 13      # only these folders

Each entry names the notebook, the claims its output must contain, and any failure
it makes on purpose. This is the file to edit when a session's headline changes --
and the one CI runs, so "it worked on my laptop" stops being the standard.
"""
import subprocess, sys, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# (folder, notebook, timeout, claims, deliberate failures)
COURSE = [
    ("01-leakage-proof-pipeline", "leakage_tutorial.ipynb", 900,
     ["optimism from group leakage", "optimism from tuning"], []),
    ("02-deep-learning", "dl_tutorial.ipynb", 2400,
     ["max diff 0.00e+00", "effective batch 64"], []),
    ("03-production-api", "api_tutorial.ipynb", 1200,
     ["cheaper per customer", "422"], []),
    ("04-docker", "docker_tutorial.ipynb", 2400,
     ["dependency change", "uid=10001(appuser)"], []),
    ("05-etl", "etl_tutorial.ipynb", 900,
     ["result: payload after 3 attempts", "rows before 1415"], []),
    ("dvc", "dvc_tutorial.ipynb", 1800,
     ["jpg files restored"], []),
    ("mlflow", "mlflow_tutorial.ipynb", 1800,
     ["registered 'churn-classifier' version 1", "runs matched", "MLflow UI stopped"],
     ["Failed to enforce schema of data"]),
    ("08-distributed-ml", "ray_tutorial.ipynb", 1800,
     ["completion order:", "each worker saw 4000 of 8000 rows"], []),
    ("09-feature-management", "feast_tutorial.ipynb", 1200,
     ["Offline and online agree to 5 decimal places"], []),
    ("10-monitoring", "monitoring_tutorial.ipynb", 2400,
     ["'firing'", "p95 latency"], []),
    ("11-automation", "automation_tutorial.ipynb", 1800,
     ["requests answered per replica pid", "'action': 'call now'"], []),
    ("12-infrastructure", "terraform_tutorial.ipynb", 2400,
     ["Plan: 2 to add, 0 to change, 0 to destroy.", "Destroy complete!"], []),
    ("13-end-to-end", "e2e_tutorial.ipynb", 1800,
     ["git_dirty is false", "the API is serving run", "built e2e-churn",
      "A container is serving the model", "Identical. From one run id",
      "container and image removed"], []),
]


def main():
    only = sys.argv[1:]
    todo = [c for c in COURSE if not only or any(o in c[0] for o in only)]
    results = []
    for folder, nb, timeout, claims, expected in todo:
        print(f"\n{'='*72}\n{folder}\n{'='*72}", flush=True)
        cmd = [sys.executable, os.path.join(HERE, "verify.py"), nb, str(timeout)]
        for c in claims: cmd += ["--claim", c]
        for e in expected: cmd += ["--expect", e]
        t0 = time.time()
        r = subprocess.run(cmd, cwd=os.path.join(ROOT, folder))
        results.append((folder, r.returncode == 0, time.time() - t0))

    print(f"\n{'='*72}")
    for folder, ok, secs in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {folder:28} {secs/60:5.1f} min")
    failed = [f for f, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} sessions pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

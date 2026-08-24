# Qafza Free Training — MLOps, from zero

Thirteen self-contained sessions. Each folder holds **a slide deck** (`*_slides.html`, one
offline file — open it in any browser) and **a notebook** (`*_tutorial.ipynb`) that runs the
same material on your machine. No prior MLOps experience assumed anywhere.

| # | Session | Core tools | Folder |
|---|---|---|---|
| 1 | Leakage-proof ML Pipeline | Python, scikit-learn | [`01-leakage-proof-pipeline`](01-leakage-proof-pipeline) |
| 2 | Deep Learning Pipeline | PyTorch, Hugging Face | `02-deep-learning` |
| 3 | Production API | FastAPI, Pydantic | [`03-production-api`](03-production-api) |
| 4 | Docker | Docker Engine | [`04-docker`](04-docker) |
| 5 | ETL Pipeline | Python, SQLAlchemy | [`05-etl`](05-etl) |
| 6 | **Versioning** | **DVC** | [`dvc`](dvc) |
| 7 | **Experiment tracking** | **MLflow** | [`mlflow`](mlflow) |
| 8 | Distributed ML | Ray Core, Ray Train | `08-distributed-ml` |
| 9 | Feature Management | Feast, Ray | `09-feature-management` |
| 10 | Monitoring | Prometheus, Grafana | `10-monitoring` |
| 11 | Automation | Ray Serve, GitHub Actions | `11-automation` |
| 12 | Infrastructure | Terraform | `12-infrastructure` |
| 13 | End-to-End ML System | the complete stack | `13-end-to-end` |

Folders without a link are not built yet.

## Using the decks

Open the `.html` file in a browser. Everything is embedded, so **no internet is needed** in
the room.

`←` `→` or `space` to move · click the left/right third of the screen · `f` fullscreen ·
`p` print (one slide per page, which is how you get a PDF)

## Using the notebooks

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Every notebook builds a **throwaway sandbox folder** beside itself, does all its work there,
and deletes it in the last cell. Nothing outside the folder is touched, and the sandboxes are
git-ignored.

Notebooks are committed **with their outputs**, so you can read the results — numbers, charts,
command output — on GitHub without running anything.

## A note on how this material is checked

Every notebook is executed end to end before it ships, and each one has to *prove its headline
claim* rather than merely run. For example session 1 must actually print a cross-validation
score of ~0.765 on data that contains no signal at all, next to the honest 0.520 — the whole
point of the session. `tools/verify.py` enforces this:

```bash
python3 tools/verify.py 01-leakage-proof-pipeline/leakage_tutorial.ipynb 900 \
        --claim "GAP:" --claim "optimism from group leakage"
```

It fails the notebook on any unexecuted cell, any exception, **any failing shell command**
(`!cmd` errors never raise in Jupyter, and have hidden two real bugs in this repo), and any
missing claim.

`tools/deck.py` and `tools/nbbuild.py` build the decks and notebooks, so a fourteenth session
is cheap to add.

## About `dvc/data.zip`

Session 6 uses a real 39 MB folder of photographs, committed here so the tutorial works the
moment you clone. That is a deliberate exception for teaching — see
[`dvc/`](dvc) — not a practice to copy.

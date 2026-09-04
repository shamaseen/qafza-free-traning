# Qafza Free Training — MLOps, from zero

Thirteen self-contained sessions. Each folder holds **a slide deck** (`*_slides.html`, one
offline file — open it in any browser) and **a notebook** (`*_tutorial.ipynb`) that runs the
same material on your machine. No prior MLOps experience assumed anywhere.

| # | Session | Core tools | Folder |
|---|---|---|---|
| 1 | Leakage-proof ML Pipeline | Python, scikit-learn | [`01-leakage-proof-pipeline`](01-leakage-proof-pipeline) |
| 2 | Deep Learning Pipeline | PyTorch, Hugging Face | [`02-deep-learning`](02-deep-learning) |
| 3 | Production API | FastAPI, Pydantic | [`03-production-api`](03-production-api) |
| 4 | Docker | Docker Engine | [`04-docker`](04-docker) |
| 5 | ETL Pipeline | Python, SQLAlchemy | [`05-etl`](05-etl) |
| 6 | **Experiment tracking** | **MLflow** | [`06-mlflow`](06-mlflow) |
| 7 | **Versioning** | **DVC** | [`07-dvc`](07-dvc) |
| 8 | Distributed ML | Ray Core, Ray Train | [`08-distributed-ml`](08-distributed-ml) |
| 9 | Feature Management | Feast | [`09-feature-management`](09-feature-management) |
| 10 | Monitoring | Prometheus, Grafana | [`10-monitoring`](10-monitoring) |
| 11 | Automation | Ray Serve, GitHub Actions | [`11-automation`](11-automation) |
| 12 | Infrastructure | Terraform | [`12-infrastructure`](12-infrastructure) |
| 13 | End-to-End ML System | the complete stack | [`13-end-to-end`](13-end-to-end) |

All thirteen are built. Session 13 is the capstone: it wires DVC, scikit-learn, MLflow,
FastAPI, Docker and CI into one chain, and then proves the chain holds by recovering a model
from nothing but its run id.

Two sessions need more than `pip`: session 4 and 13 need a running **Docker** daemon, and
session 12 needs the **Terraform** CLI. Each notebook checks for its tools in the first cells
and says so plainly if one is missing.

## Using the decks

Open the `.html` file in a browser. Everything is embedded, so **no internet is needed** in
the room.

`←` `→` or `space` to move · click the left/right third of the screen · `f` fullscreen ·
`p` print (one slide per page, which is how you get a PDF)

Two markers appear throughout: a slide tagged **skip on first read** is depth you can come back
to, and one tagged **reference — not for reading** is a lookup table, not a slide to present.
Every session defines its vocabulary in a **crash course** slide before using it — you are
expected to know Python, and nothing else.

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

Every notebook here was **executed end to end** before it shipped, and each one has to *prove its
headline claim* rather than merely run. Session 1 must actually print a cross-validation score of
0.765 on data containing no signal at all, next to the honest 0.520. Session 4 must show a code
edit rebuilding in 0.1s against a dependency edit taking 162s. Session 13 must recover a model
from nothing but a run id and get the same metric back, to six decimal places.

Three rules are enforced mechanically, because each one caught real defects while this course was
being written:

* **no unexecuted cell, no exception, and no failing shell command.** `!cmd` failures never raise
  in Jupyter, so a broken build or a rejected config looks like success unless you read the
  output. That hid two genuine bugs here.
* **every figure quoted on a slide must appear in its notebook's output.** This caught six decks
  quoting numbers their notebook never printed, and one quoting a run id from an earlier run.
* **every "deck slides 20–21" pointer must land on slides that exist.** Eleven notebooks had
  drifted past the end of their own deck after the decks were rebuilt.

Some sessions fail on purpose — session 7 renames a column to show MLflow's model signature
rejecting it — so those failures are declared, and a deliberate failure cannot quietly become an
undeclared one.

The scripts that run these checks and build the decks are kept locally rather than shipped, so
this repository stays what it is for: the material.

Session 11 builds a CI workflow that runs exactly these checks over the whole repository — see
[`11-automation/workflows/`](11-automation/workflows) for it and the one command that activates it.

## About `07-dvc/data.zip`

Session 6 uses a real 39 MB folder of photographs, committed here so the tutorial works the
moment you clone. That is a deliberate exception for teaching — see
[`07-dvc/`](07-dvc) — not a practice to copy.

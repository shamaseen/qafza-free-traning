# Qafza Free Training — DVC & MLflow

Two self-contained MLOps sessions, taught from zero. No prior DVC, MLflow or MLOps
experience assumed.

| | Slides | Notebook |
|---|---|---|
| **Data versioning** | [`dvc/dvc_slides.html`](dvc/dvc_slides.html) — 53 slides | [`dvc/dvc_tutorial.ipynb`](dvc/dvc_tutorial.ipynb) |
| **Experiment tracking** | [`mlflow/mlflow_slides.html`](mlflow/mlflow_slides.html) — 41 slides | [`mlflow/mlflow_tutorial.ipynb`](mlflow/mlflow_tutorial.ipynb) |

The two sessions are independent — take either one first.

## The slides

Open the `.html` file in any browser. Everything is embedded, so **no internet is needed**
in the room.

* `←` `→` or `space` to move, click the left/right third of the screen
* `f` fullscreen, `p` print (one slide per page — that is how you get a PDF)

## The notebooks

Each notebook is the hands-on half of its deck, and every part names the slides it covers.
Run top to bottom.

```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab            # or: jupyter notebook
```

Each notebook builds a **throwaway sandbox folder** next to itself (`dvc_demo/`,
`mlflow_demo/`), does all its work there, and has a cleanup cell at the end. Nothing outside
the folder is touched, and the sandboxes are git-ignored.

## About `data.zip`

Part 5 of the DVC notebook uses the real course dataset — `data.zip`, about 39 MB of cat and
dog photographs — to version a genuinely large folder rather than a toy CSV.

**That file is deliberately not in this repository.** Keeping 39 MB of images out of Git is
the entire lesson of the DVC session: Git carries a few hundred bytes of pointer, and the
photos live in DVC storage.

Put `data.zip` next to this repository (or in your home folder) and Part 5 finds it
automatically. Without it, Part 5 skips itself cleanly and the rest of the notebook still
runs.

## What each session covers

**DVC** — why Git breaks on data · `dvc add` and the pointer file · remotes, `push`/`pull` ·
time travel with `git checkout` + `dvc checkout` · pipelines (`dvc.yaml`, `dvc repro`) ·
metrics · DVCLive · experiments · the run cache · `.dvcignore` · `artifacts:` · credentials ·
merge conflicts · CI with CML

**MLflow** — runs, params, metrics, artifacts · the UI · sweeps and `search_runs` · autolog ·
saving and loading models properly · the Model Registry and aliases · dataset tracking ·
nested runs · custom `pyfunc` models · signatures · `mlflow.evaluate` · system metrics ·
serving · what MLflow 3 changed

## Requirements

Python 3.9+ and Git. Everything else is in `requirements.txt`.

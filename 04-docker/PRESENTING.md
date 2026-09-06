# Presenting session 4 without waiting for builds

The notebook is the right artefact to **hand out** — it really builds four images and measures
them, which is the whole point. It is the wrong artefact to **run live**: a cold build takes
about three minutes of silence, and the full notebook takes six and a half.

This file is the live path. Run the fast commands in a terminal, and read the slow numbers off
the slides — they came from the notebook, so they are real.

## Before the room

Build the images once, the night before, so everything below is instant.

Open the notebook in Jupyter and **Run All except the last cell**. That matters: the final
cleanup cell deletes the four images and the sandbox folder, which is correct for a reader and
exactly wrong for a presenter.

```bash
docker images --filter reference='churn:*'      # four images: naive, ignored, slim, multi
```

If they are missing, the cleanup cell ran. Re-run the notebook and stop before it.

## The live path — nothing here takes more than two seconds

**1. What a container is** — the shortest possible demonstration.

```bash
docker run --rm python:3.12-slim python -c "print('hello from inside a container')"
```

**2. The four images, side by side.** This is the session's headline and it is one command.

```bash
docker images --filter reference='churn:*' --format 'table {{.Tag}}\t{{.Size}}'
```

```
TAG       SIZE
naive     1.63GB
ignored   1.56GB
slim      490MB
multi     491MB
```

> **Expect a question here.** `docker images` says 1.63 GB where the notebook says 1,557 MB —
> same image. `docker images` counts in decimal (1 GB = 1,000 MB); the notebook converts the
> byte count from `docker image inspect` into MiB. Both are right. Say so and move on.

**3. Layers — why the ordering rule exists.**

```bash
docker history churn:multi --format 'table {{.Size}}\t{{.CreatedBy}}' | head -8
```

**4. Run it, and call it.** Have a second terminal open.

```bash
docker run -d --name demo -p 8000:8000 churn:multi
# port 8000 busy? "driver failed programming external connectivity" -- use -p 8080:8000
curl -s localhost:8000/health
curl -s -X POST localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"tenure_months": 2, "monthly_charge": 130.0, "support_calls": 8, "plan": "basic"}'
```

**5. It is not running as root** — the point people remember.

```bash
docker exec demo id
# uid=10001(appuser) gid=10001(appuser) groups=10001(appuser)
docker rm -f demo
```

## The numbers to read out, not reproduce

Every one of these is measured in the notebook. Quote them; do not try to produce them live.

| What | Measured |
|---|---|
| naive image | 1557.1 MB, built in 104.8 s |
| `+ .dockerignore` | 1492.1 MB — 65.0 MB from one file |
| `+ slim base, no pip cache` | 467.2 MB — 70% smaller |
| `+ multi-stage` | 468.6 MB, and no build toolchain in the image |
| cold build, no cache | 90.4 s |
| rebuild, nothing changed | 0.1 s |
| rebuild after a **code** edit | 0.1 s |
| rebuild after a **dependency** edit | 83.8 s |

That last pair is the session in two numbers: same one-line change, 1,600× apart, decided
entirely by the order of two `COPY` lines.

## If a build must happen live

Do it during a question, not during an explanation — and start it with `--no-cache` so the
number is honest:

```bash
time docker build --no-cache -f Dockerfile.multi -t churn:demo .
```

Three minutes. Take questions while it runs; do not narrate the scrolling output.

## If Docker is not available at all

Everything above degrades to the deck: the four measured sizes, the layer diagrams from Docker's
own documentation, and the cold-versus-warm build chart are all on the slides. The one thing you
lose is the live `curl` against a running container, and a screenshot of that is in the notebook
output.

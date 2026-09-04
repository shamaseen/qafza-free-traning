# Image credits

Most diagrams and every chart in this course were made for it. The diagrams below come from
the official documentation of the tools being taught, and are reused here under their licences.
Each one also carries its source and licence on the slide it appears on.

| Image | Used in | Source | Licence |
|---|---|---|---|
| Docker architecture — client, daemon, registry | `04-docker` | [docs.docker.com/get-started/docker-overview](https://docs.docker.com/get-started/docker-overview/) | Apache 2.0 — © Docker, Inc. |
| MLflow tracking setups — local, local + database, remote server | `06-mlflow` | [mlflow.org/docs/latest/self-hosting/architecture/overview](https://mlflow.org/docs/latest/self-hosting/architecture/overview/) | Apache 2.0 |
| DVC flow — workspace, cache, remote, and the git pointer | `07-dvc` | [dvc.org](https://dvc.org) | Apache 2.0 — © Iterative, Inc. |
| Container vs virtual machine (cropped to the two panels that compare) | `04-docker` | [kubernetes.io/docs/concepts/overview](https://kubernetes.io/docs/concepts/overview/) | CC BY 4.0 |
| Prometheus architecture — pull, store, query, alert | `10-monitoring` | [prometheus.io/docs/introduction/overview](https://prometheus.io/docs/introduction/overview/) | Apache 2.0 |
| Feast architecture — sources, store, online and offline serving | `09-feature-management` | [feast.dev](https://docs.feast.dev/) | Apache 2.0 |
| Image layers — the stack, and layer reuse across images | `04-docker` | [docs.docker.com/get-started/docker-concepts/building-images](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/) | Apache 2.0 — © Docker, Inc. |
| The parts of an HTTP request, and of a response | `03-production-api` | [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | CC BY-SA 2.5 — © Mozilla contributors |

Most are used unmodified; the Kubernetes one is cropped to two panels and Docker's layer
diagrams are trimmed of their white margins to its two right-hand panels, as its
licence permits with attribution. All are embedded rather than linked, so the decks keep working with no
network. Terraform's diagrams were deliberately left out: HashiCorp's licensing changed and I
could not establish a clean reuse licence for them.

Everything else — the charts, the flow diagrams, the screenshots of MLflow's UI, Grafana and
FastAPI's `/docs` — was produced by running the notebooks in this repository.

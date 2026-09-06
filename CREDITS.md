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

## Linked, not embedded

Three sources were suggested for these slides and are **linked** from the "Where to learn more"
slide of the session they belong to, rather than copied into it. All three are commercial,
all-rights-reserved work, and redistributing them inside a public repository is not something
their licences allow:

| Source | Where it is linked |
|---|---|
| [What is Docker? — OPC Router](https://www.opc-router.com/what-is-docker/) | `04-docker` — its container-vs-VM point is already covered by the CC BY 4.0 Kubernetes diagram |
| [REST vs GraphQL — ByteByteGo](https://bytebytego.com/guides/rest-api-vs-graphql/) | `03-production-api` — the comparison is redrawn for this deck in its own style |
| Rocky Bhatia's "Top 6 API architecture" post on LinkedIn | `03-production-api` — the same six styles are covered on the "other kinds" slide |

Linking credits the author and costs nothing. Embedding would have contradicted the first line of
this file.

## Learning resources

Every link on a "Where to learn more" slide was fetched before it shipped; the YouTube ones were
checked through the oEmbed endpoint, which fails for a deleted video, and the titles and channel
names on the slides are the ones it returned.

Arabic coverage is uneven and the slides say so. Docker and machine-learning fundamentals have
genuinely good Arabic courses. DVC, Feast, Ray and Terraform have effectively none, so those
slides point at the nearest useful Arabic material and state plainly that no course was found,
rather than filling the column with something weak.

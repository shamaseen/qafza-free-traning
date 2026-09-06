#!/usr/bin/env bash
# Build the example image, run it, and prove it answers. Nothing is downloaded
# beyond the python:3.12-slim base, and nothing is pip-installed at all.
#
#   ./build.sh          build, run, check, leave it running on :8500
#   ./build.sh clean    stop it and remove the image
set -euo pipefail
cd "$(dirname "$0")"

if [ "${1:-}" = "clean" ]; then
  docker rm -f churn-demo >/dev/null 2>&1 || true
  docker rmi -f churn:demo >/dev/null 2>&1 || true
  echo "removed."; exit 0
fi

docker info >/dev/null 2>&1 || { echo "the docker daemon is not running - see PRESENTING.html"; exit 1; }

docker build -t churn:demo .
docker rm -f churn-demo >/dev/null 2>&1 || true
docker run -d --name churn-demo -p 8500:8000 churn:demo >/dev/null

for _ in $(seq 20); do curl -sf localhost:8500/health >/dev/null && break; sleep 0.2; done

echo
echo "health   $(curl -s localhost:8500/health)"
echo "predict  $(curl -s -X POST localhost:8500/predict -H 'Content-Type: application/json' \
                 -d '{"tenure_months":2,"monthly_charge":130,"support_calls":8}')"
echo "user     $(docker exec churn-demo id)"
echo "size     $(docker images churn:demo --format '{{.Size}}')"
echo
echo "running on http://localhost:8500  -  ./build.sh clean when you are done"

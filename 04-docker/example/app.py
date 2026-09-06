"""A tiny prediction API. Standard library only -- nothing to install."""
import json
import math
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = "1.0.0"


def predict(f):
    # ponytail: a hand-written rule, not a trained model. This session is about the
    # container, not the maths -- swap in joblib.load() when it is about the maths.
    score = (-1.5
             + 0.35 * f["support_calls"]
             + 0.02 * f["monthly_charge"]
             - 0.04 * f["tenure_months"])
    return round(1 / (1 + math.exp(-score)), 2)   # squash into 0..1


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, body):
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/health":
            self.reply(200, {"status": "ok", "version": VERSION})
        else:
            self.reply(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/predict":
            return self.reply(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", 0))
        try:
            p = predict(json.loads(self.rfile.read(length)))
        except (ValueError, TypeError, KeyError) as e:
            return self.reply(422, {"error": f"bad input: {e}"})
        self.reply(200, {"churn": p > 0.5, "probability": p, "version": VERSION})

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)


if __name__ == "__main__":
    print(f"listening on 0.0.0.0:8000 (version {VERSION})", flush=True)
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()

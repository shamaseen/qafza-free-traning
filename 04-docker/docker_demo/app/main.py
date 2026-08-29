"""A small model API -- the artifact we are going to package."""
import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional

MODEL_PATH = os.getenv("MODEL_PATH", "app/model.joblib")
STATE = {}

app = FastAPI(title="Churn API", version="1.0.0")


class Customer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tenure_months:  int   = Field(ge=0, le=600)
    monthly_charge: float = Field(ge=0, le=10_000)
    support_calls:  int   = Field(ge=0, le=100)
    plan: Literal["basic", "plus", "pro"]


@app.on_event("startup")
def load():
    STATE["b"] = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    b = STATE.get("b")
    return {"status": "ok" if b else "degraded", "model_loaded": b is not None,
            "model_version": b["version"] if b else None}


@app.post("/predict")
def predict(c: Customer):
    b = STATE.get("b")
    if b is None:
        raise HTTPException(503, "model not loaded")
    frame = pd.DataFrame([c.model_dump()])[b["features"]]
    p = float(b["pipeline"].predict_proba(frame)[0, 1])
    return {"churn": p >= .5, "probability": round(p, 4), "model_version": b["version"]}

# a one-line change, like any Tuesday

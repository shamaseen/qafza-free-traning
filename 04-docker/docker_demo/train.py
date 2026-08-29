"""Produces app/model.joblib. Runs on the host, not in the image."""
import numpy as np, pandas as pd, joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

rng = np.random.default_rng(0); m = 3000
df = pd.DataFrame({"tenure_months": rng.integers(1, 72, m),
                   "monthly_charge": rng.normal(65, 20, m).round(2),
                   "support_calls": rng.poisson(1.2, m),
                   "plan": rng.choice(["basic", "plus", "pro"], m)})
s = (-0.04*df.tenure_months + 0.03*df.monthly_charge + 0.55*df.support_calls
     + rng.normal(0, .8, m))
y = (s > s.mean()).astype(int)
NUM, CAT = ["tenure_months", "monthly_charge", "support_calls"], ["plan"]
pipe = Pipeline([("pre", ColumnTransformer([
                    ("num", Pipeline([("i", SimpleImputer()), ("s", StandardScaler())]), NUM),
                    ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])),
                 ("model", RandomForestClassifier(n_estimators=100, random_state=0))]).fit(df[NUM+CAT], y)
joblib.dump({"pipeline": pipe, "version": "1.0.0", "features": NUM + CAT}, "app/model.joblib")
print("wrote app/model.joblib")

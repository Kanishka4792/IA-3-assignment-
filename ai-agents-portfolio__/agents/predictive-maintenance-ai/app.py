import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

st.title("Predictive Maintenance AI")
st.caption("Sample sensor data. Predicts which machines may fail soon and picks a maintenance day.")

# ---- 1. Sample sensor history with failure labels
rng = np.random.default_rng(9)
n = 3000
hist = pd.DataFrame({
    "temperature": rng.normal(70, 10, n),
    "vibration": rng.normal(3, 1, n),
    "current": rng.normal(15, 3, n),
    "load_pct": rng.normal(60, 15, n),
})
z = -10 + 0.05 * hist.temperature + 0.8 * hist.vibration + 0.1 * hist.current + 0.03 * hist.load_pct
hist["fails_within_7_days"] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)

# ---- 2. Train
feats = ["temperature", "vibration", "current", "load_pct"]
X_tr, X_te, y_tr, y_te = train_test_split(hist[feats], hist.fails_within_7_days,
                                          test_size=0.25, random_state=0, stratify=hist.fails_within_7_days)
model = RandomForestClassifier(100, max_depth=6, class_weight="balanced", random_state=0).fit(X_tr, y_tr)
st.metric("Model quality (ROC-AUC on unseen data)", f"{roc_auc_score(y_te, model.predict_proba(X_te)[:, 1]):.2f}")
st.bar_chart(pd.Series(model.feature_importances_, index=feats).sort_values())

# ---- 3. Today's machines
machines = pd.DataFrame({
    "machine": [f"M{i}" for i in range(1, 11)],
    "temperature": rng.normal(75, 12, 10), "vibration": rng.normal(3.5, 1.2, 10),
    "current": rng.normal(16, 3, 10), "load_pct": rng.normal(65, 15, 10),
    "criticality_1to5": rng.integers(1, 6, 10),
})
machines["failure_risk"] = model.predict_proba(machines[feats])[:, 1].round(2)
machines["priority"] = (machines.failure_risk * machines.criticality_1to5).round(2)
thr = st.slider("Alert when failure risk is above", 0.05, 0.9, 0.3)
machines["alert"] = np.where(machines.failure_risk >= thr, "ALERT", "")
st.dataframe(machines.sort_values("priority", ascending=False).round(1))

# ---- 4. Best maintenance day = day with the lowest planned production
schedule = pd.Series(rng.integers(40, 100, 7), index=[f"Day {d}" for d in range(1, 8)], name="planned production %")
st.bar_chart(schedule)
st.info(f"Schedule maintenance on **{schedule.idxmin()}** (lowest production load). "
        "Start with the machines at the top of the priority table.")

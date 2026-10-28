import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

st.title("Customer Churn & Retention Intelligence")
st.caption("Sample data. Predicts who will leave, groups them, and suggests a retention action.")

# ---- 1. Sample customers
rng = np.random.default_rng(2)
n = 1500
df = pd.DataFrame({
    "tenure_months": rng.integers(1, 60, n),
    "monthly_charge": rng.normal(70, 20, n).clip(20, 150),
    "support_tickets": rng.poisson(1.5, n),
    "usage_drop_pct": rng.uniform(0, 80, n),
})
z = -4.2 + 0.03 * df.monthly_charge + 0.35 * df.support_tickets + 0.03 * df.usage_drop_pct - 0.03 * df.tenure_months
df["churned"] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)

# ---- 2. Train a churn model
features = ["tenure_months", "monthly_charge", "support_tickets", "usage_drop_pct"]
scaler = StandardScaler().fit(df[features])
X = scaler.transform(df[features])
X_tr, X_te, y_tr, y_te = train_test_split(X, df.churned, test_size=0.25, random_state=0)
model = LogisticRegression().fit(X_tr, y_tr)
st.metric("Model quality (ROC-AUC on unseen customers)", f"{roc_auc_score(y_te, model.predict_proba(X_te)[:, 1]):.2f}")
df["risk"] = model.predict_proba(X)[:, 1]

# ---- 3. Pick the at-risk customers
thr = st.slider("Risk threshold", 0.1, 0.9, 0.4)
risky = df[df.risk >= thr].copy()
st.write(f"**{len(risky)}** of {n} customers are at risk (overall churn rate: {df.churned.mean():.0%}).")

# ---- 4. Group at-risk customers and suggest an action for each group
if len(risky) >= 3:
    risky["segment"] = KMeans(3, n_init=10, random_state=0).fit_predict(scaler.transform(risky[features]))
    summary = risky.groupby("segment")[features].mean().round(1)
    summary["customers"] = risky.segment.value_counts().sort_index()
    st.dataframe(summary)
    actions = {"monthly_charge": "Offer a discount or cheaper plan",
               "support_tickets": "Call the customer and fix the service problems",
               "usage_drop_pct": "Send a re-engagement campaign showing unused features",
               "tenure_months": "Run a new-customer onboarding programme"}
    for seg, row in summary.iterrows():
        scores = {f: (row[f] - df[f].mean()) / df[f].std() for f in features}
        scores["tenure_months"] = -scores["tenure_months"]  # low tenure = new customer
        main = max(scores, key=scores.get)
        st.success(f"Segment {seg} ({int(row.customers)} customers) - main driver: **{main}** -> {actions[main]}")

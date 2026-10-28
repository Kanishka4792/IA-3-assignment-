import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

st.title("Employee Attrition Root-Cause Intelligence")
st.caption("Sample data. Shows which factors are linked to people leaving and tests a retention idea.")

# ---- 1. Sample employees
rng = np.random.default_rng(5)
n = 1200
df = pd.DataFrame({
    "department": rng.choice(["Sales", "Tech", "HR", "Operations"], n),
    "overtime_hours": rng.uniform(0, 30, n),
    "satisfaction": rng.integers(1, 6, n),
    "salary_k": rng.normal(60, 15, n).clip(25, 120),
    "years_at_company": rng.integers(0, 15, n),
    "absent_days": rng.poisson(4, n),
    "training_hours": rng.uniform(0, 60, n),
})
z = -2 + 0.08 * df.overtime_hours - 0.6 * (df.satisfaction - 3) - 0.03 * (df.salary_k - 60) - 0.05 * df.years_at_company
df["left"] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)

# ---- 2. Attrition rate by department
st.subheader("Attrition rate by department")
st.bar_chart(df.groupby("department").left.mean())

# ---- 3. Which factors matter? (standardised logistic regression)
feats = ["overtime_hours", "satisfaction", "salary_k", "years_at_company", "absent_days", "training_hours"]
sc = StandardScaler().fit(df[feats])
X_tr, X_te, y_tr, y_te = train_test_split(sc.transform(df[feats]), df.left, test_size=0.25, random_state=0)
model = LogisticRegression().fit(X_tr, y_tr)
st.metric("Model quality (ROC-AUC on unseen employees)", f"{roc_auc_score(y_te, model.predict_proba(X_te)[:, 1]):.2f}")
coef = pd.Series(model.coef_[0], index=feats).sort_values()
st.subheader("Factor strength (negative = protects against leaving)")
st.bar_chart(coef)
st.caption("These are associations to investigate, not proof of cause.")

# ---- 4. What if we cut overtime?
cut = st.slider("Reduce overtime by (%)", 0, 100, 30)
sim = df[feats].copy()
sim["overtime_hours"] *= 1 - cut / 100
before = model.predict_proba(sc.transform(df[feats]))[:, 1].mean()
after = model.predict_proba(sc.transform(sim))[:, 1].mean()
c1, c2 = st.columns(2)
c1.metric("Predicted attrition now", f"{before:.1%}")
c2.metric("Predicted attrition after", f"{after:.1%}", f"{after - before:.1%}")
st.warning("This is a model estimate with assumptions. Test it with a pilot before rolling it out. "
           "The tool only advises; people make the decisions.")

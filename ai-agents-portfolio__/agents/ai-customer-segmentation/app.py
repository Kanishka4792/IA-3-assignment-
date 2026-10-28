import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

st.title("AI Customer Segmentation")
st.caption("Sample data. Groups customers by behaviour (RFM) and suggests a strategy per group.")

# ---- 1. Sample customers: Recency, Frequency, Monetary
rng = np.random.default_rng(4)
n = 1000
df = pd.DataFrame({
    "recency_days": rng.exponential(60, n).round() + 1,
    "frequency": rng.poisson(5, n) + 1,
    "monetary": rng.lognormal(6, 0.6, n).round(),
})

# ---- 2. Cluster
k = st.slider("Number of segments", 2, 6, 4)
X = StandardScaler().fit_transform(np.log1p(df))
df["segment"] = KMeans(k, n_init=10, random_state=0).fit_predict(X)
st.metric("Cluster quality (silhouette, higher is better)", f"{silhouette_score(X, df.segment):.2f}")

# ---- 3. Describe and label each segment
summary = df.groupby("segment").mean().round(1)
summary["customers"] = df.segment.value_counts().sort_index()
med = df[["recency_days", "frequency", "monetary"]].median()

def label(r):
    if r.recency_days < med.recency_days and r.frequency > med.frequency and r.monetary > med.monetary:
        return "Champions"
    if r.recency_days > med.recency_days and r.frequency < med.frequency:
        return "At-risk / lapsed"
    if r.monetary > med.monetary:
        return "Big spenders"
    return "Occasional buyers"

strategy = {"Champions": "Reward with loyalty perks and early access",
            "At-risk / lapsed": "Win-back offer with a time-limited discount",
            "Big spenders": "Upsell premium products and bundles",
            "Occasional buyers": "Nudge with reminders and small incentives"}
summary["label"] = summary.apply(label, axis=1)
summary["recommended strategy"] = summary.label.map(strategy)
st.dataframe(summary)
st.scatter_chart(df, x="frequency", y="monetary", color="segment")

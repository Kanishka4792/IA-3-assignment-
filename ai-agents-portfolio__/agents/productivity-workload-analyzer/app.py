import numpy as np
import pandas as pd
import streamlit as st

st.title("Employee Productivity vs. Workload")
st.caption("Sample data. Finds teams that work more hours but get less done.")

# ---- 1. Sample data: 6 teams x 20 weeks. Output per hour falls once hours go above 42.
rng = np.random.default_rng(7)
base_hours = {"Team A": 38, "Team B": 40, "Team C": 44, "Team D": 47, "Team E": 50, "Team F": 52}
weekly_tasks = {"Team A": 70, "Team B": 72, "Team C": 80, "Team D": 85, "Team E": 90, "Team F": 92}  # new tasks per week
rows = []
for team, base in base_hours.items():
    backlog = 0.0
    for week in range(1, 21):
        hours = rng.normal(base, 2)
        done = hours * 2 * (1 - 0.03 * max(0, hours - 42)) * rng.normal(1, 0.03)
        backlog = max(0, backlog + weekly_tasks[team] - done)
        absent = rng.poisson(1 + max(0, hours - 40) * 0.2)
        rows.append([team, week, hours, done, done / hours, absent, backlog])
df = pd.DataFrame(rows, columns=["team", "week", "hours", "tasks_done", "tasks_per_hour", "absent_days", "backlog"])

# ---- 2. Team summary
def trend(g):
    return np.polyfit(g.week, g.tasks_per_hour, 1)[0]

s = df.groupby("team").agg(avg_hours=("hours", "mean"), tasks_per_hour=("tasks_per_hour", "mean"),
                           absent_days=("absent_days", "mean"), final_backlog=("backlog", "last"))
s["productivity_trend"] = df.groupby("team").apply(trend)
s["flag"] = np.where((s.avg_hours > 45) | (s.final_backlog > 100), "Overloaded / bottleneck", "OK")
st.dataframe(s.round(2))

st.subheader("Hours worked vs output per hour")
st.scatter_chart(df, x="hours", y="tasks_per_hour", color="team")
st.write(f"Correlation between hours and absence: **{df.hours.corr(df.absent_days):.2f}**")

# ---- 3. Recommendations
for team, r in s[s.flag != "OK"].iterrows():
    st.error(f"{team}: {r.avg_hours:.0f} hrs/week, backlog {r.final_backlog:.0f} tasks. "
             "Rebalance tasks to teams with spare capacity, cut meetings, or add support staff.")

"""
ML Signals page — RL weights, complexity scorer, demand forecast internals.
"""
import random
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="ML Signals · BaristaIQ", layout="wide", page_icon="☕")

st.markdown("## 🤖 ML Signals")

col1, col2, col3 = st.columns(3)

# ── RL policy weights ─────────────────────────────────────────────────────────
with col1:
    st.markdown("#### RL policy weights")
    weights = {
        "wait_time": 0.88,
        "complexity": 0.72,
        "concurrency_fit": 0.91,
        "machine_load": 0.45,
        "milk_type": 0.63,
        "shot_count": 0.38,
    }
    for k, v in weights.items():
        st.markdown(f"**{k.replace('_', ' ')}** — `{v:.2f}`")
        st.progress(v)

    st.divider()
    st.markdown("#### Training stats")
    st.metric("Episodes (30d)", "1,847")
    st.metric("Avg reward (last 100)", "+1.84")
    st.metric("Policy improvement", "+78% vs random")

# ── Q-values ──────────────────────────────────────────────────────────────────
with col2:
    st.markdown("#### Q-values by action")
    q_vals = {
        "batch_milk_steams": 0.91,
        "maximize_concurrency": 0.88,
        "prioritize_wait_time": 0.82,
        "reorder_by_score": 0.74,
        "use_idle_machine": 0.68,
        "prioritize_complexity": 0.55,
    }
    for action, qv in q_vals.items():
        c1, c2 = st.columns([3, 1])
        with c1:
            st.progress(qv, text=action.replace("_", " "))
        with c2:
            st.markdown(f"`{qv:.2f}`")

    st.divider()
    st.markdown("#### Reward history (today)")
    rewards = [random.gauss(1.4, 0.9) for _ in range(60)]
    df = pd.DataFrame({"reward": rewards, "zero": [0]*60})
    st.area_chart(df[["reward"]], height=120, color="#22c55e")

# ── Complexity matrix ─────────────────────────────────────────────────────────
with col3:
    st.markdown("#### Drink complexity matrix")
    from core.scorer.complexity_scorer import score_all_presets
    results = score_all_presets()
    rows = []
    for name, r in sorted(results.items(), key=lambda x: x[1].total, reverse=True):
        rows.append({
            "Drink": r.extraction_seconds,
            "Score": r.total,
            "Tier": r.tier.upper(),
            "Slots": r.concurrent_slots_needed,
            "Label": r.label,
        })
    df2 = pd.DataFrame(rows, index=[r.label for r in sorted(results.values(), key=lambda x: x.total, reverse=True)])
    st.dataframe(df2[["Score", "Tier", "Slots"]], use_container_width=True)

    st.divider()
    st.markdown("#### Demand forecast model")
    hours = list(range(6, 22))
    demand = [1, 2, 5, 12, 18, 14, 8, 6, 10, 14, 8, 5, 4, 4, 3, 2]
    fig = go.Figure(go.Bar(x=[f"{h}:00" for h in hours], y=demand, marker_color=["#f59e0b" if 8 <= h <= 9 else "#2a2a32" for h in hours]))
    fig.update_layout(height=160, margin=dict(t=0, b=20, l=20, r=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True)

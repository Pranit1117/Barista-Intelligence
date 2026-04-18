"""
Config & Calibration page.
"""
import streamlit as st

st.set_page_config(page_title="Config · BaristaIQ", layout="wide", page_icon="☕")
st.markdown("## ⚙️ Config & Calibration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Machine calibration")
    with st.form("machine_form"):
        st.slider("Group 1 shot time (s)", 18, 35, 28)
        st.slider("Group 2 shot time (s)", 18, 35, 27)
        st.slider("Steamer warm-up (s)", 5, 20, 8)
        st.slider("Grinder time (s)", 6, 18, 10)
        st.slider("Assemble time (s)", 8, 25, 15)
        st.divider()
        st.markdown("**Milk steam times (seconds)**")
        st.slider("Whole milk", 15, 45, 24)
        st.slider("Oat milk", 15, 50, 32)
        st.slider("Almond milk", 15, 50, 30)
        st.slider("Soy milk", 15, 45, 28)
        if st.form_submit_button("Save machine config", type="primary"):
            st.success("Machine config saved!")

with col2:
    st.markdown("#### Feature toggles")
    st.toggle("Rush mode auto-activation", value=True, help="Activates when >8 orders/min detected")
    st.toggle("Concurrent suggestions", value=True, help="Show 'while that pulls' prompts")
    st.toggle("RL live retraining", value=True, help="Update policy weights from completions")
    st.toggle("Demand forecasting", value=True, help="Weather + calendar signals")
    st.toggle("Post-rush auto-report", value=True, help="Generate scorecard after each rush")
    st.toggle("Error recovery mode", value=False, help="Re-queue on parse or machine fault")

    st.divider()
    st.markdown("#### Demand model inputs")
    st.toggle("Time-of-day signal", value=True)
    st.toggle("Day-of-week signal", value=True)
    st.toggle("Weather signal (rainy = +18%)", value=True)
    st.toggle("Local events calendar", value=False)

    st.divider()
    st.markdown("#### RL training")
    with st.form("rl_form"):
        st.slider("Learning rate (α)", 0.001, 0.1, 0.03, 0.001, format="%.3f")
        st.slider("Discount factor (γ)", 0.80, 0.99, 0.95, 0.01, format="%.2f")
        st.slider("Exploration rate (ε)", 0.01, 0.40, 0.12, 0.01, format="%.2f")
        if st.form_submit_button("Save RL config"):
            st.success("RL config saved!")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Export config JSON", use_container_width=True):
            import json
            cfg = {"machine": {"g1": 28, "g2": 27}, "rl": {"lr": 0.03, "gamma": 0.95, "eps": 0.12}}
            st.download_button("Download config.json", json.dumps(cfg, indent=2), "barista_iq_config.json")
    with c2:
        if st.button("Reset to defaults", use_container_width=True, type="secondary"):
            st.warning("This will reset all calibration values.")

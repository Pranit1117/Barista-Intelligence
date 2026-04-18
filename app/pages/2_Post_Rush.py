"""Post-Rush Report · BaristaIQ — Premium café design"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Post-Rush · BaristaIQ", layout="wide", page_icon="☕")

PAGE_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
:root{--cream:#FBF7F1;--linen:#EFE6D5;--foam:#E8DDD0;--latte:#D4B896;--caramel:#C49A6C;
  --espresso:#3D2314;--roast:#5C3317;--mocha:#7B4A2D;--bark:#9B6B47;--steam:#8A7560;
  --copper:#B5712A;--sage:#4A7C59;--rush:#C0392B;
  --shadow-sm:0 1px 3px rgba(61,35,20,0.08),0 1px 2px rgba(61,35,20,0.04);
  --shadow-md:0 4px 16px rgba(61,35,20,0.10);--r-md:12px;--r-lg:18px;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;color:var(--espresso)!important;}
.stApp{background-color:var(--cream)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:32px 32px 48px!important;max-width:100%!important;}
.topbar{background:var(--espresso);padding:0 32px;height:62px;display:flex;align-items:center;
  justify-content:space-between;margin:-32px -32px 32px;
  box-shadow:0 2px 20px rgba(61,35,20,0.45);}
.topbar-logo{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;
  color:var(--latte)!important;letter-spacing:-0.5px;}
.topbar-logo span{color:var(--caramel)!important;}
.topbar-sub{font-size:10px;color:rgba(212,184,150,0.5)!important;letter-spacing:.14em;
  text-transform:uppercase;border-left:1px solid rgba(212,184,150,0.18);padding-left:14px;}
.section-eyebrow{font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--bark)!important;margin-bottom:9px;display:flex;align-items:center;gap:8px;}
.section-eyebrow::after{content:'';flex:1;height:1px;background:linear-gradient(to right,var(--linen),transparent);}
.card{background:white;border:1px solid var(--foam);border-radius:var(--r-md);
  padding:20px 22px;box-shadow:var(--shadow-sm);margin-bottom:12px;}
.card-title{font-family:'Playfair Display',serif;font-size:14px;font-weight:600;
  color:var(--espresso)!important;margin-bottom:14px;}
.big-num{font-family:'Playfair Display',serif;font-size:44px;font-weight:700;line-height:1;}
.insight-card{background:white;border-left:3px solid var(--caramel);border-radius:0 var(--r-md) var(--r-md) 0;
  padding:12px 16px;margin-bottom:8px;box-shadow:var(--shadow-sm);
  border-top:1px solid var(--foam);border-right:1px solid var(--foam);border-bottom:1px solid var(--foam);}
.insight-label{font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:var(--copper)!important;margin-bottom:4px;}
.insight-text{font-size:12px;color:var(--mocha)!important;line-height:1.5;}
.bar-row{display:flex;align-items:center;gap:10px;margin-bottom:7px;}
.bar-lbl{font-size:11px;color:var(--steam)!important;flex:0 0 130px;}
.bar-track{flex:1;height:5px;background:var(--linen);border-radius:3px;overflow:hidden;}
.bar-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--caramel),var(--copper));}
.bar-val{font-family:'DM Mono',monospace;font-size:11px;color:var(--mocha)!important;
  width:30px;text-align:right;}
[data-testid="stMetric"]{background:white;border:1px solid var(--foam);
  border-radius:var(--r-md);padding:13px 15px!important;box-shadow:var(--shadow-sm);}
[data-testid="stMetricLabel"]{color:var(--steam)!important;font-size:10px!important;
  letter-spacing:.06em;text-transform:uppercase;font-weight:600!important;}
[data-testid="stMetricValue"]{font-family:'Playfair Display',serif!important;
  color:var(--espresso)!important;font-size:22px!important;}
hr{border:none!important;border-top:1px solid var(--foam)!important;margin:18px 0!important;}
</style><link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
"""
st.markdown(PAGE_STYLES, unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
  <div style="display:flex;align-items:center;gap:14px">
    <div class="topbar-logo">Barista<span>IQ</span></div>
    <div class="topbar-sub">Post-Rush Report</div>
  </div>
  <div style="font-family:'DM Mono',monospace;font-size:12px;color:rgba(212,184,150,0.6)">
    7:45 AM – 9:15 AM
  </div>
</div>""", unsafe_allow_html=True)

# Score gauge
col_score, col_metrics = st.columns([1, 2.2], gap="large")

with col_score:
    st.markdown('<div class="section-eyebrow">🏆 Session Score</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=84,
        title={"text": "Peak Handling Score", "font": {"size": 12, "color": "#8A7560", "family": "DM Sans"}},
        gauge={
            "axis": {"range": [0,100], "tickwidth": 0, "tickcolor": "#EFE6D5",
                     "tickfont": {"color":"#8A7560","size":9}},
            "bar": {"color": "#4A7C59", "thickness": 0.24},
            "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
            "steps": [
                {"range":[0,50],  "color":"rgba(192,57,43,0.10)"},
                {"range":[50,75], "color":"rgba(212,136,30,0.10)"},
                {"range":[75,100],"color":"rgba(74,124,89,0.10)"},
            ],
            "threshold": {"line": {"color": "#C49A6C","width": 2}, "thickness": 0.75, "value": 84}
        },
        number={"suffix":"/100","font":{"size":36,"color":"#3D2314","family":"Playfair Display"}},
    ))
    fig.update_layout(height=230, margin=dict(t=30,b=0,l=20,r=20),
                      paper_bgcolor="rgba(0,0,0,0)", font_family="DM Sans")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="card" style="text-align:center">'
                '<div style="font-size:10px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;'
                'color:var(--steam);margin-bottom:8px">Time Saved vs Serial</div>'
                '<div class="big-num" style="color:var(--sage)">81m</div>'
                '<div style="font-size:11px;color:var(--bark);margin-top:5px">across 67 orders</div>'
                '</div>', unsafe_allow_html=True)

with col_metrics:
    st.markdown('<div class="section-eyebrow">📈 Rush Summary</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Orders Served", "67", "+19 vs baseline")
    with m2: st.metric("Time Saved",    "81m", "vs serialized")
    with m3: st.metric("Avg Wait",      "4.2m", "Was 6.4m")
    with m4: st.metric("Revenue Uplift","₹2,280", "This rush only")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-eyebrow">📊 Throughput vs Baseline</div>', unsafe_allow_html=True)

    hours = [f"7:{h:02d}" for h in range(45,60,5)] + [f"8:{h:02d}" for h in range(0,60,5)] + [f"9:{h:02d}" for h in range(0,20,5)]
    baseline  = [3,4,6,9,11,14,16,15,14,12,10,8,6,5,4,3,2,2,2]
    baristaiq = [4,6,9,14,18,22,25,24,22,18,15,12,9,7,5,4,3,3,2]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=hours, y=baseline, name="Baseline",
        line=dict(color="rgba(138,117,96,0.4)", dash="dot", width=1.5)))
    fig2.add_trace(go.Scatter(x=hours, y=baristaiq, name="BaristaIQ",
        line=dict(color="#4A7C59", width=2.5),
        fill="tozeroy", fillcolor="rgba(74,124,89,0.07)"))
    fig2.update_layout(
        height=190, margin=dict(t=5,b=20,l=30,r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#8A7560", size=10),
        legend=dict(orientation="h", y=1.12, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor="rgba(239,230,213,0.8)",
                   title="orders/5min", titlefont=dict(size=9)),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<div class="section-eyebrow">💡 Coach Insights</div>', unsafe_allow_html=True)
    for label, color, text in [
        ("Best Moment",          "#4A7C59", "3 concurrent orders at 8:47 AM — flat white + cold brew + oat latte in flight simultaneously. 2.3 min compression."),
        ("Missed Opportunity",   "#D4881E", "At 8:12 AM, steamer idle 47s while espresso pulled. Concurrent milk steam would have saved ~40s across 4 drinks."),
        ("Model Updated",        "#B5712A", "Oat milk steam time recalibrated 28s → 32s from 14 new completions. Policy weights adjusted."),
    ]:
        st.markdown(f"""
<div class="insight-card" style="border-left-color:{color}">
  <div class="insight-label" style="color:{color}!important">{label}</div>
  <div class="insight-text">{text}</div>
</div>""", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-eyebrow">🌤 Tomorrow\'s Forecast</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="card">
  <div style="font-size:14px;font-weight:600;color:var(--espresso);margin-bottom:12px">
    Wednesday · Overcast · Mid-week
  </div>
  <div style="font-size:13px;color:var(--mocha);line-height:1.8">
    <span style="color:var(--copper);font-weight:600">High demand likely</span> —
    62 orders forecast 7:30–9:30 AM<br>
    Peak window: <strong style="color:var(--espresso)">8:40–8:55 AM</strong><br>
    <span style="color:var(--sage);font-weight:500">Rec:</span>
    Pre-warm both groups by 7:25 AM
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-eyebrow" style="margin-top:4px">🤖 Model Accuracy</div>',
                unsafe_allow_html=True)
    for drink, acc, color in [("Latte", 94, "#4A7C59"), ("Cappuccino", 91, "#4A7C59"),
                                ("Cold brew", 76, "#D4881E"), ("Oat flat white", 68, "#D4881E")]:
        st.markdown(f"""
<div class="bar-row">
  <span class="bar-lbl">{drink}</span>
  <div class="bar-track"><div class="bar-fill" style="width:{acc}%;background:{color}"></div></div>
  <span class="bar-val">{acc}%</span>
</div>""", unsafe_allow_html=True)

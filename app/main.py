"""
BaristaIQ — Premium Café Intelligence System
World-class UI redesign: warm parchment · espresso ink · craft-coffee editorial aesthetic
"""
import time
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(
    page_title="BaristaIQ · Brew Smarter",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;900&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Mono:wght@400;500&display=swap');

:root {
  --parchment:#F7F0E6;--cream:#FBF7F1;--linen:#EFE6D5;--latte:#D4B896;
  --caramel:#C49A6C;--espresso:#3D2314;--roast:#5C3317;--mocha:#7B4A2D;
  --bark:#9B6B47;--steam:#8A7560;--foam:#E8DDD0;--copper:#B5712A;
  --amber:#D4881E;--sage:#4A7C59;--sage-light:rgba(74,124,89,0.10);
  --sage-border:rgba(74,124,89,0.30);--rush:#C0392B;
  --rush-light:rgba(192,57,43,0.10);--rush-border:rgba(192,57,43,0.28);
  --amber-light:rgba(212,136,30,0.10);--amber-border:rgba(212,136,30,0.28);
  --shadow-sm:0 1px 3px rgba(61,35,20,0.08),0 1px 2px rgba(61,35,20,0.04);
  --shadow-md:0 4px 16px rgba(61,35,20,0.10),0 2px 6px rgba(61,35,20,0.05);
  --r-sm:6px;--r-md:12px;--r-lg:18px;
}

html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;color:var(--espresso)!important;}
.stApp{background-color:var(--cream)!important;
  background-image:radial-gradient(ellipse at 15% 0%,rgba(196,154,108,0.10) 0%,transparent 55%),
  radial-gradient(ellipse at 85% 100%,rgba(91,51,23,0.07) 0%,transparent 50%);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none;}

.topbar{background:var(--espresso);padding:0 32px;height:62px;display:flex;
  align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;
  box-shadow:0 2px 20px rgba(61,35,20,0.45);}
.topbar-brand{display:flex;align-items:center;gap:14px;}
.topbar-logo{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;
  color:var(--latte)!important;letter-spacing:-0.5px;}
.topbar-logo span{color:var(--caramel)!important;}
.topbar-tagline{font-size:10.5px;color:rgba(212,184,150,0.5)!important;font-weight:300;
  letter-spacing:0.14em;text-transform:uppercase;border-left:1px solid rgba(212,184,150,0.18);
  padding-left:14px;}
.topbar-right{display:flex;align-items:center;gap:18px;}
.topbar-time{font-family:'DM Mono',monospace;font-size:13px;color:var(--latte)!important;
  letter-spacing:0.04em;}
.rush-pill{display:inline-flex;align-items:center;gap:7px;background:var(--rush-light);
  border:1px solid var(--rush-border);color:#E05C4A!important;padding:5px 14px;
  border-radius:20px;font-size:10.5px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;}
.rush-dot{width:7px;height:7px;border-radius:50%;background:#E05C4A;
  box-shadow:0 0 7px rgba(224,92,74,0.8);animation:blink 1.4s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.35;transform:scale(0.72);}}

.main-canvas{padding:26px 30px 48px;}

.section-eyebrow{font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;
  color:var(--bark)!important;margin-bottom:9px;display:flex;align-items:center;gap:8px;}
.section-eyebrow::after{content:'';flex:1;height:1px;
  background:linear-gradient(to right,var(--linen),transparent);}
.section-title{font-family:'Playfair Display',serif;font-size:15px;font-weight:600;
  color:var(--espresso)!important;margin-bottom:14px;margin-top:0;}

.order-card{background:white;border:1px solid var(--foam);border-radius:var(--r-md);
  padding:11px 13px;margin-bottom:7px;box-shadow:var(--shadow-sm);
  position:relative;overflow:hidden;transition:transform 0.15s,box-shadow 0.15s;}
.order-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
  background:var(--foam);border-radius:3px 0 0 3px;}
.order-card.active{border-color:var(--sage-border);background:var(--sage-light);}
.order-card.active::before{background:var(--sage);}
.order-card.nextup{border-color:var(--amber-border);background:var(--amber-light);}
.order-card.nextup::before{background:var(--amber);}
.order-id{font-family:'DM Mono',monospace;font-size:10px;color:var(--steam)!important;font-weight:500;}
.order-name{font-size:13px;font-weight:600;color:var(--espresso)!important;margin:2px 0 1px;}
.order-drinks{font-size:11px;color:var(--mocha)!important;}
.wait-chip{font-family:'DM Mono',monospace;font-size:10px;background:var(--linen);
  color:var(--roast)!important;padding:2px 7px;border-radius:4px;font-weight:500;}
.wait-chip.urgent{background:var(--rush-light);color:var(--rush)!important;}
.cdot{width:8px;height:8px;border-radius:50%;display:inline-block;}

.action-now{background:linear-gradient(140deg,#2A5230 0%,#3A7040 100%);
  border-radius:var(--r-lg);padding:22px 24px;margin-bottom:11px;
  box-shadow:0 8px 32px rgba(42,82,48,0.28),var(--shadow-md);position:relative;overflow:hidden;}
.action-now::before{content:'';position:absolute;top:-50px;right:-30px;width:130px;height:130px;
  border-radius:50%;background:rgba(255,255,255,0.04);}
.action-now::after{content:'';position:absolute;bottom:-25px;right:16px;width:90px;height:90px;
  border-radius:50%;background:rgba(255,255,255,0.03);}
.action-eyebrow{font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;
  color:rgba(255,255,255,0.5)!important;margin-bottom:9px;display:flex;align-items:center;gap:7px;}
.action-pulse{width:7px;height:7px;border-radius:50%;background:#7DD87D;
  box-shadow:0 0 9px rgba(125,216,125,0.9);animation:blink 1.2s ease-in-out infinite;}
.action-headline{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;
  color:white!important;line-height:1.35;margin-bottom:5px;}
.action-detail{font-size:12px;color:rgba(255,255,255,0.55)!important;letter-spacing:0.02em;}

.action-concurrent{background:white;border:1.5px solid var(--amber-border);
  border-radius:var(--r-md);padding:15px 19px;margin-bottom:11px;box-shadow:var(--shadow-sm);}
.conc-eyebrow{font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
  color:var(--copper)!important;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
.conc-headline{font-size:14px;font-weight:600;color:var(--espresso)!important;margin-bottom:2px;}
.conc-detail{font-size:11px;color:var(--steam)!important;}

.stButton>button{border-radius:var(--r-sm)!important;font-family:'DM Sans',sans-serif!important;
  font-weight:600!important;font-size:13px!important;padding:10px 20px!important;
  transition:all 0.15s ease!important;border:none!important;}
.stButton>button[kind="primary"]{background:var(--espresso)!important;color:var(--latte)!important;
  box-shadow:0 4px 12px rgba(61,35,20,0.22)!important;}
.stButton>button[kind="primary"]:hover{background:var(--roast)!important;
  transform:translateY(-1px)!important;box-shadow:0 6px 18px rgba(61,35,20,0.30)!important;}
.stButton>button:not([kind]){background:white!important;color:var(--roast)!important;
  border:1.5px solid var(--foam)!important;}
.stButton>button:not([kind]):hover{background:var(--linen)!important;
  border-color:var(--latte)!important;transform:translateY(-1px)!important;}

.machine-card{background:white;border:1px solid var(--foam);border-radius:var(--r-md);
  padding:12px 14px;margin-bottom:7px;box-shadow:var(--shadow-sm);}
.machine-name{font-size:10px;font-weight:700;letter-spacing:0.10em;text-transform:uppercase;
  color:var(--steam)!important;margin-bottom:3px;}
.machine-status{font-size:13px;font-weight:600;color:var(--espresso)!important;margin-bottom:7px;}
.machine-status.ready{color:var(--sage)!important;}
.machine-status.busy{color:var(--copper)!important;}

.stProgress>div>div>div>div{
  background:linear-gradient(90deg,var(--caramel),var(--copper))!important;border-radius:4px!important;}
.stProgress>div>div>div{background:var(--linen)!important;border-radius:4px!important;height:5px!important;}

.schedule-row{display:flex;align-items:center;gap:10px;padding:7px 11px;
  border-radius:var(--r-sm);margin-bottom:4px;transition:background 0.15s;}
.schedule-row:hover{background:var(--linen);}
.schedule-row.now-row{background:var(--sage-light);}
.sched-time{font-family:'DM Mono',monospace;font-size:10px;color:var(--steam)!important;
  width:36px;flex-shrink:0;}
.sched-machine{font-size:10px;font-weight:700;padding:2px 7px;border-radius:4px;
  background:var(--linen);color:var(--roast)!important;white-space:nowrap;flex-shrink:0;}
.sched-action{font-size:12px;color:var(--espresso)!important;flex:1;}
.sched-order{font-family:'DM Mono',monospace;font-size:10px;color:var(--bark)!important;}

.signal-row{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.signal-label{font-size:11px;color:var(--steam)!important;flex:0 0 106px;font-weight:400;}
.signal-track{flex:1;height:5px;background:var(--linen);border-radius:3px;overflow:hidden;}
.signal-fill{height:100%;border-radius:3px;
  background:linear-gradient(90deg,var(--caramel),var(--copper));transition:width 0.8s ease;}
.signal-val{font-family:'DM Mono',monospace;font-size:11px;color:var(--mocha)!important;
  width:30px;text-align:right;}

.stream-box{background:var(--espresso);border-radius:var(--r-md);padding:13px 15px;
  font-family:'DM Mono',monospace;font-size:10.5px;line-height:1.8;}
.sl-order{color:#A8D5A2;}
.sl-event{color:rgba(212,184,150,0.55);}
.sl-rush{color:#E8A97E;}

hr{border:none!important;border-top:1px solid var(--foam)!important;margin:14px 0!important;}

[data-testid="stMetric"]{background:white;border:1px solid var(--foam);
  border-radius:var(--r-md);padding:13px 15px!important;box-shadow:var(--shadow-sm);}
[data-testid="stMetricLabel"]{color:var(--steam)!important;font-size:10px!important;
  letter-spacing:0.06em;text-transform:uppercase;font-weight:600!important;}
[data-testid="stMetricValue"]{font-family:'Playfair Display',serif!important;
  color:var(--espresso)!important;font-size:22px!important;}
[data-testid="stMetricDelta"]{font-size:10px!important;}

::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--latte);border-radius:3px;}

details>summary{background:white;border:1px solid var(--foam)!important;
  border-radius:var(--r-md)!important;padding:10px 14px;color:var(--roast)!important;
  font-weight:600;font-size:12px;cursor:pointer;}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
"""

st.markdown(STYLES, unsafe_allow_html=True)

# ── Core imports ──────────────────────────────────────────────────────────────
from core.scheduler.concurrent_scheduler import ConcurrentScheduler, make_action_text
from core.scorer.complexity_scorer import score_drink
from core.pos.mock_stream import generate_rush_batch, generate_order

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("orders", None), ("completed", 0), ("time_saved", 0.0),
              ("reward", 47.3), ("g1", 28), ("g2", 27),
              ("w_wait", 0.70), ("w_cplx", 0.20), ("w_mach", 0.10),
              ("stream_log", [
                  ("08:22", "ORDER_IN #112 · Priya M. · Oat latte", "order"),
                  ("08:22", "ORDER_IN #113 · Rohan K. · Flat white, Cold brew", "order"),
                  ("08:23", "complexity #112 → 7.2 [high]", "event"),
                  ("08:23", "ORDER_IN #114 · Aisha T. · Cappuccino", "order"),
                  ("08:23", "RUSH MODE — queue depth 9", "rush"),
              ])]:
    if k not in st.session_state:
        st.session_state[k] = generate_rush_batch(9) if k == "orders" else v

scheduler = ConcurrentScheduler(
    wait_weight=st.session_state.w_wait,
    complexity_weight=st.session_state.w_cplx,
    machine_weight=st.session_state.w_mach,
    group1_shot_secs=st.session_state.g1,
    group2_shot_secs=st.session_state.g2,
)
active_orders = [o for o in st.session_state.orders if not o.is_complete]
result = scheduler.schedule(active_orders)
action_main, action_sub, conc_main, conc_sub = make_action_text(result)
is_rush = len(active_orders) >= 6

# ── Top bar ───────────────────────────────────────────────────────────────────
rush_html = ('<div class="rush-pill"><div class="rush-dot"></div>Rush Hour Active</div>'
             if is_rush else "")
st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">
    <div class="topbar-logo">Barista<span>IQ</span></div>
    <div class="topbar-tagline">Brew Intelligence Platform</div>
  </div>
  <div class="topbar-right">
    {rush_html}
    <div class="topbar-time">{time.strftime('%I:%M %p')} &nbsp;·&nbsp; {len(active_orders)} in queue</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main canvas ───────────────────────────────────────────────────────────────
st.markdown('<div class="main-canvas">', unsafe_allow_html=True)
col_left, col_center, col_right = st.columns([1.05, 1.45, 1.0], gap="medium")

# ═══════════════════ LEFT: Queue ══════════════════════════════════════════════
with col_left:
    st.markdown('<div class="section-eyebrow">☕ Today\'s Brew</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Optimized Queue</div>', unsafe_allow_html=True)

    if st.button("＋  New Order", use_container_width=True):
        new = generate_order(random.randint(300, 999))
        st.session_state.orders.append(new)
        st.session_state.stream_log.append((
            time.strftime('%H:%M'),
            f"ORDER_IN {new.order_id} · {new.customer_name} · {', '.join(d.name for d in new.drinks)}",
            "order"
        ))
        st.rerun()

    for i, order in enumerate(active_orders[:10]):
        complexity = score_drink(order.drinks[0]) if order.drinks else None
        score_val  = complexity.total if complexity else 0
        dot_color  = "#4A7C59" if score_val < 5 else "#D4881E" if score_val < 7 else "#C0392B"
        card_cls   = "active" if i == 0 else "nextup" if i == 1 else ""
        status_tag = "▶ Now" if i == 0 else "Next" if i == 1 else f"#{i+1}"
        drinks_str = "  ·  ".join(d.name for d in order.drinks)
        wait_cls   = "urgent" if order.wait_minutes > 5 else ""
        st.markdown(f"""
<div class="order-card {card_cls}">
  <div style="display:flex;align-items:flex-start;justify-content:space-between">
    <div>
      <div class="order-id">{order.order_id} &nbsp;·&nbsp; {status_tag}</div>
      <div class="order-name">{order.customer_name}</div>
      <div class="order-drinks">{drinks_str}</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;padding-top:2px">
      <div class="wait-chip {wait_cls}">{order.wait_minutes}m</div>
      <div class="cdot" style="background:{dot_color}"></div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════ CENTER: Command ══════════════════════════════════════════
with col_center:
    st.markdown('<div class="section-eyebrow">⚡ Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">What to Make Next</div>', unsafe_allow_html=True)

    headline = action_main if action_main else "Queue is clear — well done!"
    st.markdown(f"""
<div class="action-now">
  <div class="action-eyebrow"><div class="action-pulse"></div>Start Right Now</div>
  <div class="action-headline">{headline}</div>
  <div class="action-detail">{action_sub}</div>
</div>""", unsafe_allow_html=True)

    if conc_main:
        st.markdown(f"""
<div class="action-concurrent">
  <div class="conc-eyebrow"><span>⟳</span>While that pulls</div>
  <div class="conc-headline">{conc_main}</div>
  <div class="conc-detail">{conc_sub}</div>
</div>""", unsafe_allow_html=True)

    b1, b2 = st.columns([3, 2])
    with b1:
        if st.button("✓  Mark Complete", type="primary", use_container_width=True):
            if active_orders:
                active_orders[0].completed_at = time.time()
                st.session_state.completed += 1
                st.session_state.time_saved += random.uniform(1.5, 2.8)
                st.session_state.reward     += random.uniform(0.5, 1.8)
                st.rerun()
    with b2:
        if st.button("Skip  →", use_container_width=True):
            if len(st.session_state.orders) > 1:
                st.session_state.orders.append(st.session_state.orders.pop(0))
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-eyebrow">🔧 Machine State</div>', unsafe_allow_html=True)

    machines = [
        ("Group 1", "Pulling shot",   68, "busy"),
        ("Group 2", "Ready",         100, "ready"),
        ("Steamer",  "Oat milk 165ml", 42, "busy"),
        ("Cold Tap", "Ready · 4°C",  100, "ready"),
    ]
    mc1, mc2 = st.columns(2)
    for idx, (name, status, pct, state) in enumerate(machines):
        with (mc1 if idx % 2 == 0 else mc2):
            st.markdown(f"""
<div class="machine-card">
  <div class="machine-name">{name}</div>
  <div class="machine-status {state}">{status}</div>
</div>""", unsafe_allow_html=True)
            st.progress(pct / 100)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-eyebrow">📋 Execution Plan</div>', unsafe_allow_html=True)

    if result.scheduled:
        for idx, slot in enumerate(result.scheduled[:7]):
            t       = slot.start_offset_secs
            t_label = "now" if t == 0 else f"+{t}s"
            machine = slot.machine_slot.replace("_", " ").title()
            row_cls = "now-row" if idx == 0 else ""
            st.markdown(f"""
<div class="schedule-row {row_cls}">
  <span class="sched-time">{t_label}</span>
  <span class="sched-machine">{machine}</span>
  <span class="sched-action">{slot.drink.name}</span>
  <span class="sched-order">{slot.order_id}</span>
</div>""", unsafe_allow_html=True)

# ═══════════════════ RIGHT: Intelligence ══════════════════════════════════════
with col_right:
    st.markdown('<div class="section-eyebrow">📊 Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Live Performance</div>', unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        st.metric("Throughput", "23/hr", "+4 vs base")
        st.metric("Queue", str(len(active_orders)),
                  "↑ growing" if len(active_orders) > 6 else "↓ easing")
    with r2:
        st.metric("Avg Wait", "4.1m", "−2.1m")
        st.metric("Concurrency", f"{result.concurrency_ratio:.1f}×", "optimal")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-eyebrow">🧠 RL Reward Signal</div>', unsafe_allow_html=True)

    reward_val = st.session_state.reward
    completed  = st.session_state.completed
    saved      = st.session_state.time_saved
    st.markdown(f"""
<div style="background:white;border:1px solid var(--foam);border-radius:var(--r-md);
  padding:15px 17px;box-shadow:var(--shadow-sm);margin-bottom:10px">
  <div style="font-size:10px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;
    color:var(--steam);margin-bottom:7px">Cumulative Reward · 30m window</div>
  <div style="font-family:'Playfair Display',serif;font-size:30px;font-weight:700;
    color:var(--sage);line-height:1">+{reward_val:.1f}</div>
  <div style="font-size:11px;color:var(--bark);margin-top:6px">
    {completed} orders done &nbsp;·&nbsp; {saved:.1f}m saved
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-eyebrow">⚖️ Policy Weights</div>', unsafe_allow_html=True)

    for label, val in [("Wait time", 0.88), ("Complexity", 0.72),
                       ("Concurrency", 0.91), ("Machine load", 0.45)]:
        st.markdown(f"""
<div class="signal-row">
  <span class="signal-label">{label}</span>
  <div class="signal-track"><div class="signal-fill" style="width:{int(val*100)}%"></div></div>
  <span class="signal-val">{val:.2f}</span>
</div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-eyebrow">📡 POS Stream</div>', unsafe_allow_html=True)

    cls_map = {"order": "sl-order", "rush": "sl-rush", "event": "sl-event"}
    lines = "".join(
        f'<div class="{cls_map.get(kind,"sl-event")}">'
        f'<span style="opacity:0.4">{ts}</span>  {msg}</div>'
        for ts, msg, kind in reversed(st.session_state.stream_log[-6:])
    )
    st.markdown(f'<div class="stream-box">{lines}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    with st.expander("⚙️  Quick Config"):
        st.session_state.g1 = st.slider("Group 1 shot (s)", 18, 35, st.session_state.g1, key="cg1")
        st.session_state.g2 = st.slider("Group 2 shot (s)", 18, 35, st.session_state.g2, key="cg2")
        st.session_state.w_wait = st.slider("Wait weight", 0.0, 1.0, st.session_state.w_wait, 0.05, key="cww")
        st.session_state.w_cplx = st.slider("Complexity weight", 0.0, 1.0, st.session_state.w_cplx, 0.05, key="cwc")
        if st.button("Apply Config", type="primary"):
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

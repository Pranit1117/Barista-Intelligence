# ☕ BaristaIQ — Barista Intelligence System

> **Every other tool tells you what happened. BaristaIQ tells your barista what to do next — while the rush is happening.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-red)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🧠 What it does

BaristaIQ is an ML-powered barista assistant that solves a real operations problem: during a 7:45–9:15 AM rush, a skilled barista makes dozens of implicit decisions — pulling two espressos simultaneously, steaming milk while shots extract. An untrained barista serializes everything. **The difference is 2–3 minutes per order. With 40 orders in rush hour, that's 80+ minutes of lost throughput daily.**

### Core capabilities

| Module | What it does |
|--------|-------------|
| **Complexity Scorer** | Scores every drink 0–10 on 5 features: extraction, milk type, customizations, temp, shot count |
| **Concurrent Scheduler** | Greedy algorithm assigns drinks to machine slots optimally — not in received order |
| **Demand Predictor** | Time + weather + day-of-week model forecasts order volume 15 min ahead |
| **RL Feedback Loop** | Completion signals retrain the policy weights in real time |
| **Barista Tablet UI** | Streamlit dashboard showing "Start now" + "While that pulls" concurrent suggestions |

---

## 🗂 Project structure

```
barista-iq/
├── app/                        # Streamlit frontend
│   ├── main.py                 # App entry point
│   ├── components/
│   │   ├── live_queue.py       # Active order queue display
│   │   ├── action_display.py   # "Start now" + concurrent suggestion
│   │   ├── machine_state.py    # Machine progress bars
│   │   ├── metrics_panel.py    # Live throughput metrics
│   │   ├── demand_chart.py     # Forecast visualization
│   │   └── post_rush_report.py # Post-rush scorecard
│   ├── pages/
│   │   ├── 1_Live_Queue.py     # Main barista view
│   │   ├── 2_Post_Rush.py      # Analytics & report
│   │   ├── 3_ML_Signals.py     # RL weights + model internals
│   │   └── 4_Config.py         # Calibration & toggles
│   └── utils/
│       ├── state.py            # Streamlit session state helpers
│       └── formatting.py       # Display formatters
│
├── core/                       # Business logic (framework-agnostic)
│   ├── scheduler/
│   │   ├── __init__.py
│   │   ├── concurrent_scheduler.py   # Main greedy scheduler
│   │   ├── priority_scorer.py        # Order priority scoring
│   │   └── slot_manager.py           # Machine slot tracking
│   ├── scorer/
│   │   ├── __init__.py
│   │   ├── complexity_scorer.py      # Drink complexity model
│   │   └── feature_extractor.py      # Feature engineering
│   ├── rl/
│   │   ├── __init__.py
│   │   ├── agent.py                  # Q-learning agent
│   │   ├── environment.py            # Café environment simulation
│   │   ├── reward.py                 # Reward shaping functions
│   │   └── trainer.py                # Training loop
│   └── pos/
│       ├── __init__.py
│       ├── stream_listener.py        # POS WebSocket listener
│       ├── order_parser.py           # Order normalization
│       └── mock_stream.py            # Dev mode order generator
│
├── api/                        # FastAPI backend
│   ├── main.py                 # FastAPI app
│   ├── routes/
│   │   ├── orders.py           # POST /orders, GET /queue
│   │   ├── scheduler.py        # GET /schedule, POST /complete
│   │   ├── metrics.py          # GET /metrics, GET /forecast
│   │   └── config.py           # GET/POST /config
│   ├── models/
│   │   ├── order.py            # Pydantic order models
│   │   ├── schedule.py         # Schedule response models
│   │   └── config.py           # Config models
│   └── dependencies.py         # Shared DI (DB, state)
│
├── data/
│   ├── raw/                    # Raw POS exports (gitignored)
│   ├── processed/              # Feature-engineered datasets
│   │   └── sample_orders.csv   # Sample data for dev/demo
│   └── models/                 # Serialized model weights
│       ├── complexity_scorer.pkl
│       └── rl_policy.pkl
│
├── tests/
│   ├── unit/
│   │   ├── test_scorer.py
│   │   ├── test_scheduler.py
│   │   └── test_rl_agent.py
│   └── integration/
│       ├── test_api.py
│       └── test_full_pipeline.py
│
├── notebooks/
│   ├── 01_EDA.ipynb            # Exploratory data analysis
│   ├── 02_complexity_model.ipynb
│   ├── 03_rl_training.ipynb
│   └── 04_demand_forecasting.ipynb
│
├── scripts/
│   ├── train_scorer.py         # Train complexity scorer
│   ├── train_rl.py             # Train RL agent
│   ├── simulate_rush.py        # Generate synthetic rush data
│   └── export_report.py        # Generate PDF report from logs
│
├── .github/
│   └── workflows/
│       ├── ci.yml              # Test + lint on PR
│       └── deploy.yml          # Deploy to Streamlit Cloud
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quick start

### Option A — Streamlit Cloud (recommended for demo)
```bash
# 1. Fork this repo on GitHub
# 2. Go to share.streamlit.io → New app → point to app/main.py
# Done. No server required.
```

### Option B — Local development
```bash
git clone https://github.com/YOUR_USERNAME/barista-iq
cd barista-iq

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env

# Run Streamlit app
streamlit run app/main.py
```

### Option C — Docker
```bash
docker-compose up
# App at http://localhost:8501
# API at http://localhost:8000/docs
```

---

## 🔧 Configuration

Copy `.env.example` → `.env` and set:

```env
# POS Integration
POS_STREAM_URL=ws://your-pos-system/orders
POS_API_KEY=your_key_here

# Mode
DEMO_MODE=true          # Use mock order stream (no POS needed)
RUSH_HOUR_START=07:45
RUSH_HOUR_END=09:15

# RL
RL_LIVE_TRAINING=true   # Update weights from completions
RL_CHECKPOINT_PATH=data/models/rl_policy.pkl

# Machine calibration (seconds)
GROUP1_SHOT_TIME=28
GROUP2_SHOT_TIME=27
STEAMER_WARMUP=8
```

---

## 📊 Business impact

| Metric | Value |
|--------|-------|
| Avg wait reduction | **2–3 min/order during peak** |
| Additional orders/rush hour | **+12–18** (70-seat café estimate) |
| Additional annual revenue | **~₹8L+** from throughput alone |
| Training time to proficiency | Days, not months |

---

## 🤝 Contributing

1. Fork → feature branch → PR
2. Run `pytest tests/` before pushing
3. Follow the [CONTRIBUTING.md](docs/CONTRIBUTING.md) guide

---

## 📄 License

MIT — see [LICENSE](LICENSE)

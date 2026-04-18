# BaristaIQ

> Every other tool tells you what happened. BaristaIQ tells your barista what to do next, while the rush is happening.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-red)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-green)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/tests-52%20passing-brightgreen)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## The problem

During a 7:45 to 9:15 AM rush, a skilled barista makes dozens of implicit decisions: pulling two espressos simultaneously, steaming milk while shots extract. An untrained barista serializes everything. The difference is 2 to 3 minutes per order. With 40 orders in rush hour, that is 80+ minutes of lost throughput daily. No existing tool tells your team what to do next, in real time, while the rush is happening.

---

## What it does

BaristaIQ is a full-stack ML system that watches the order queue, scores each drink by complexity, schedules concurrent machine usage optimally, and surfaces a single clear action to the barista: **start this now** and **while that pulls, do this**.

### Five core modules

| Module | What it does |
|---|---|
| **Complexity Scorer** | Scores every drink 0 to 10 across extraction method, milk type, customizations, temperature, and shot count. Powder-prep drinks like matcha carry a bonus step for whisking and vessel prep. |
| **Concurrent Scheduler** | Greedy algorithm assigns drinks to machine slots in priority order, maximising parallel execution. No two drinks ever collide on the same machine. Produces a live action pair: start now + while that pulls. |
| **RL Feedback Loop** | Tabular Q-learning agent updates policy weights with every order completion. Reward is shaped across throughput gain, wait reduction, concurrency bonus, and order error penalty. Checkpoint save and load included. |
| **POS Stream** | WebSocket listener normalises real POS payloads. In demo mode, a mock generator produces orders on a realistic rush-hour demand curve with configurable rate, multiplier, and error injection. |
| **Demand Forecaster** | Time-of-day, day-of-week, and weather signals predict volume 15 minutes ahead. Powers rush-mode auto-activation and pre-warm recommendations shown in the post-rush report. |

---

## Business impact

| Metric | Value |
|---|---|
| Avg wait reduction per order at peak | 2 to 3 minutes |
| Additional orders served per rush hour | +12 to 18 (70-seat cafe estimate) |
| Daily throughput recovered vs serialized | ~80 minutes |
| Additional annual revenue potential | ~Rs 8L+ |
| Time to barista proficiency | Days, not months |

---

## Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.35, multi-page, custom CSS design system, Plotly |
| Backend | FastAPI + Uvicorn, Pydantic v2, full OpenAPI docs at /docs |
| ML core | NumPy, scikit-learn, Gymnasium, tabular Q-learning |
| Testing | pytest, 52 tests (38 unit + 14 integration), FastAPI TestClient |
| DevOps | Docker, docker-compose, GitHub Actions CI on every PR |
| Data | Pandas, joblib, model checkpoint serialisation |

---

## Project structure

```
barista-iq/
├── app/                    # Streamlit frontend
│   ├── main.py             # Entry point
│   └── pages/              # Post-rush report · ML signals · Config
├── core/                   # Framework-agnostic business logic
│   ├── scorer/             # Complexity scorer
│   ├── scheduler/          # Concurrent greedy scheduler
│   ├── rl/                 # Q-learning agent + reward shaping
│   └── pos/                # POS stream listener + mock generator
├── api/                    # FastAPI routes: /orders /schedule /metrics /config
├── tests/
│   ├── unit/               # scorer · scheduler · RL agent
│   └── integration/        # full pipeline + all API endpoints
├── scripts/                # train_scorer.py · train_rl.py
├── notebooks/              # EDA · complexity model · RL training
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## Quick start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/barista-iq
cd barista-iq

# Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run
streamlit run app/main.py
```

Opens at `localhost:8501`. Runs in demo mode by default, no POS connection needed.

```bash
# Run tests
pytest tests/

# Run with API (optional)
docker-compose up
# Streamlit at :8501 · FastAPI at :8000/docs
```

---

## Configuration

Copy `.env.example` to `.env`. Key variables:

```env
DEMO_MODE=true                          # Use mock order stream
RUSH_HOUR_START=07:45
RUSH_HOUR_END=09:15
GROUP1_SHOT_TIME=28                     # Machine calibration (seconds)
GROUP2_SHOT_TIME=27
RL_LIVE_TRAINING=true                   # Update weights from completions
```

All machine times, scheduler weights, and RL hyperparameters are tunable from the Config page in the UI without touching code.

---

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to share.streamlit.io and sign in with GitHub
3. Select your repo, set main file to `app/main.py`, click Deploy

Live in under 3 minutes. Free.

---

## Contributing

Fork, create a feature branch, run `pytest tests/` before opening a PR. The GitHub Actions CI workflow runs all 52 tests automatically on every push.

---

## License

MIT. See [LICENSE](LICENSE).

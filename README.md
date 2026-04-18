# ☕ BaristaIQ

> Every other tool tells you what happened. BaristaIQ tells your barista what to do next, while the rush is happening.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-red)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Live Demo

👉 **Try it here:**
**https://barista-intelligence-dgws2xgnfvb7pabavthwu6.streamlit.app/**

*No setup needed. Runs in demo mode with live simulated café orders.*

---

## 🧠 The problem

During a 7:45 to 9:15 AM rush, a skilled barista makes dozens of implicit decisions: pulling two espressos simultaneously, steaming milk while shots extract.
An untrained barista serializes everything.

The difference is **2–3 minutes per order**.

With 40 orders in rush hour, that’s **80+ minutes of lost throughput daily**.

---

## ⚡ What it does

BaristaIQ is a real-time decision system that:

* Watches incoming orders
* Scores each drink by complexity
* Optimizes machine usage with concurrent scheduling
* Tells the barista exactly what to do

👉 **Start this now**
👉 **While that pulls, do this**

---

## 🔑 Core system

| Module                   | What it does                                                                       |
| ------------------------ | ---------------------------------------------------------------------------------- |
| **Complexity Scorer**    | Scores drinks 0–10 based on extraction, milk, customizations, temp, and shot count |
| **Concurrent Scheduler** | Assigns drinks to machine slots for parallel execution                             |
| **RL Feedback Loop**     | Learns better sequencing from real completions                                     |
| **POS Stream (Mock)**    | Simulates real café rush with dynamic order flow                                   |
| **Demand Forecaster**    | Predicts order volume 15 minutes ahead                                             |

---

## 📊 Business impact

| Metric                | Value            |
| --------------------- | ---------------- |
| Wait time reduction   | 2–3 min/order    |
| Extra orders per rush | +12 to 18        |
| Throughput recovered  | ~80 min/day      |
| Revenue impact        | ~₹8L+/year       |
| Training time         | Days, not months |

---

## 🛠 Tech stack

* **Frontend:** Streamlit (multi-page dashboard)
* **Backend:** FastAPI
* **ML:** scikit-learn, NumPy
* **RL:** Q-learning (Gymnasium)
* **Data:** Pandas
* **Infra:** Docker, GitHub Actions

---

## 🧱 Project structure

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
---

## 🎯 Why this is different

Most tools:
Show analytics after the rush

BaristaIQ:
 Acts **during the rush**
 Gives **real-time decisions**
 Improves **throughput, not just visibility**

---

## 📸 Demo

<img width="812" height="480" alt="image" src="https://github.com/user-attachments/assets/d4f60b36-2d49-4c2f-b0be-ddfcce061eef" />




---

## 📄 License

MIT

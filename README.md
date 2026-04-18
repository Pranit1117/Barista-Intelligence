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
├── app/            # Streamlit UI
├── core/           # ML + scheduling logic
├── api/            # FastAPI backend
├── scripts/        # Training scripts
├── tests/          # Unit + integration tests
```

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

<img width="539" height="233" alt="image" src="https://github.com/user-attachments/assets/d637bb08-a17c-4eff-b4f3-b6b233e816b6" />


---

## 📄 License

MIT

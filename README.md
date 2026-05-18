# 🛡️ CPUTracker: Real-Time Anomaly Detection Engine

A hybrid backend and data science microservice that ingests real-time system performance metrics (CPU, Memory, Latency), flags anomalous spikes using an unsupervised Machine Learning model, and visualizes system health metrics.

## 🚀 System Architecture

1. **Ingestion API:** Built with **FastAPI** to handle incoming system metric payloads asynchronously via background workers.
2. **Analytics Engine:** Utilizes **Scikit-Learn's Isolation Forest** algorithm to evaluate incoming multi-dimensional data points against learned baselines.
3. **Persistence Layer:** Logs all metrics and anomaly flags to a local **SQLite** database using **SQLAlchemy ORM**.
4. **Automated Feedback Loop:** Tracks incoming request counts to trigger automatic model re-training pipelines when data baseline thresholds are crossed.
5. **Monitoring UI:** A pure-Python interactive dashboard built with **Streamlit** and **Plotly** to view live system health and historical alerts.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy
- **Data Science:** Scikit-Learn, Pandas, NumPy
- **Frontend & Visualization:** Streamlit, Plotly Express
- **Infrastructure:** Docker (Multi-platform `linux/arm64` support)

---

## 📦 Quick Start

### Running Locally with Docker

This project is fully containerized and configured to build seamlessly across architectures, including Apple Silicon Mac (`arm64`) and Windows/Linux (`amd64`).

1. **Build the Docker Image:**
   ```bash
   docker build --platform linux/arm64 -t cputracker .
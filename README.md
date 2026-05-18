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

2. **Run Container:**
    ```bash
    docker run -p 8000:8000 -p 8501:8501 cputracker

3. **Explore the App:**
   - Interactive UI: `http://localhost:8501`
   - API Sandbox (Swagger Docs): `http://localhost:8000/docs`

---

## 💡 Key Engineering Challenges Solved

### Thread-Safe Database Writes in Asynchronous Contexts
**Challenge:** FastAPI's background tasks run outside the main request-response cycle, creating potential database session collisions when logging fast-moving metric data.
**Solution:** Implemented explicit session handling context managers within the background executor (`analyze_and_save`), ensuring every isolated background thread opens, commits, and cleanly closes its own database connection.

### Seamless Multi-Platform Containerization
**Challenge:** Environment and pathing discrepancies when transitioning the application stack from global Windows environments to Apple Silicon containerized environments (`linux/arm64`).
**Solution:** Bypassed shell binary lookup limitations by refactoring the container entry point instructions to use explicit `python -m` module wrappers, ensuring cross-platform package execution reliability.
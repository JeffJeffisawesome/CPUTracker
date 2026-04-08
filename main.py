from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

# --- DATABASE SETUP ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./metrics.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MetricLogs(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    cpu_usage = Column(Float)
    mem_usage = Column(Float)
    latency = Column(Float)
    is_anomaly = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ML MODEL SETUP ---
app = FastAPI(title="Sentinel Anomaly API")
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(np.random.normal(size=(100, 3)))

# --- SCHEMAS ---
class Metric(BaseModel):
    cpu_usage: float
    mem_usage: float
    latency: float

# --- ENDPOINTS ---
@app.post("/ingest")
async def ingest_metric(data: Metric, background_tasks: BackgroundTasks):
    background_tasks.add_task(analyze_and_save, data)
    return {"status": "processing"}

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    # Returns the last 10 entries from the DB
    return db.query(MetricLogs).order_by(MetricLogs.timestamp.desc()).limit(10).all()

# --- LOGIC ---
counter = 0
def analyze_and_save(data: Metric):
    global counter
    db = SessionLocal()
    input_features = [[data.cpu_usage, data.mem_usage, data.latency]]
    prediction = model.predict(input_features)
    is_anomaly = True if prediction[0] == -1 else False
    
    # Save to Database
    new_log = MetricLogs(
        cpu_usage=data.cpu_usage,
        mem_usage=data.mem_usage,
        latency=data.latency,
        is_anomaly=is_anomaly
    )
    db.add(new_log)
    db.commit()
    db.close()
    
    counter += 1
    if counter >= 50:
        print("retraining")
        retrain_model()
        counter = 0
    
    if is_anomaly:
        print(f"!!! ANOMALY SAVED TO DB !!!")

def retrain_model():
    global model
    db = SessionLocal()
    # Pull the last 100 entries to "re-tune" the model
    logs = db.query(MetricLogs).order_by(MetricLogs.timestamp.desc()).limit(100).all()
    db.close()
    
    if len(logs) < 10:
        return # Not enough data to retrain yet
    
    # Convert DB objects to a format Scikit-Learn understands
    data = [[log.cpu_usage, log.mem_usage, log.latency] for log in logs]
    new_df = pd.DataFrame(data)
    
    # Re-fit the model on the latest data
    model.fit(new_df)
    print(f"--- Model Retrained on {len(logs)} samples at {datetime.now()} ---")
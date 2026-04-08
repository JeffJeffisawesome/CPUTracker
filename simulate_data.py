import requests
import random
import time

url = "http://127.0.0.1:8000/ingest"

print("Starting data simulation... Press Ctrl+C to stop.")

while True:
    # 90% chance of normal data, 10% chance of an anomaly
    if random.random() > 0.1:
        data = {
            "cpu_usage": random.uniform(10, 40),
            "mem_usage": random.uniform(20, 50),
            "latency": random.uniform(20, 100)
        }
    else:
        # Generate an anomaly
        data = {
            "cpu_usage": random.uniform(85, 100),
            "mem_usage": random.uniform(80, 95),
            "latency": random.uniform(1000, 5000)
        }
    
    try:
        requests.post(url, json=data)
        print(f"Sent: {data['cpu_usage']:.1f}% CPU | Anomaly: {data['latency'] > 500}")
    except:
        print("API is offline. Make sure uvicorn is running!")
    
    time.sleep(1) # Send a request every second
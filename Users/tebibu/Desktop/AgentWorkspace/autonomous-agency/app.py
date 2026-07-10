import time
import json
import csv
import threading
import os
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# --- 1. ENTERPRISE TELEMETRY ---
def log_telemetry(action, status):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {action}: {status}")
    # Write to a persistent file for audit tracking
    with open("system_journal.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), action, status])

class AgentState(BaseModel):
    task_id: str = "NONE"
    status: str = "IDLE"

# --- 2. ORCHESTRATION ENGINE ---
class OrchestrationEngine:
    def __init__(self):
        self.state = AgentState()
        
    def health_check(self):
        return "OPERATIONAL"

    def process_batch(self, task_name):
        self.state.task_id = task_name
        self.state.status = "PROCESSING"
        log_telemetry(f"TASK_START: {task_name}", "ACTIVE")
        
        # Simulate high-throughput processing
        time.sleep(2) 
        
        self.state.status = "COMPLETED"
        log_telemetry(f"TASK_END: {task_name}", "SUCCESS")
        return True

    def run_batch_file(self, filepath):
        try:
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    tasks = [line.strip() for line in file if line.strip()]
                    for task in tasks:
                        self.process_batch(task)
                self.state.task_id = "BATCH_COMPLETE"
                self.state.status = "IDLE"
            else:
                log_telemetry("BATCH_LOAD", "ERROR: tasks.txt not found")
        except Exception as e:
            log_telemetry("BATCH_EXECUTION", f"ERROR: {str(e)}")

engine = OrchestrationEngine()

# --- 3. API BRIDGE ---
@app.get("/status")
def get_system_metrics():
    return {
        "system_health": engine.health_check(),
        "task_id": engine.state.task_id,
        "status": engine.state.status,
        "timestamp": datetime.now().isoformat()
    }

def start_server():
    # Cloud-ready: Uses PORT from environment, defaults to 8000 for local
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start API server in background so the engine can run tasks simultaneously
    threading.Thread(target=start_server, daemon=True).start()
    print("🚀 Enterprise Orchestration Engine Online.")
    
    # Run the batch ingestor
    engine.run_batch_file("tasks.txt")
    
    # Keep the engine alive
    while True:
        time.sleep(1)
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]  # Allow all for testing

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    soil_moisture: int
    tank_level: float
    pump_status: bool

latest_data = {}
latest_command = "none"

@app.post("/esp32/data")
def receive_data(data: SensorData):
    global latest_data
    latest_data = data.dict()
    print("Received data:", latest_data)
    return {"status": "success"}

@app.get("/esp32/data/latest")
def get_latest_data():
    return latest_data if latest_data else {"message": "No data available"}

@app.get("/esp32/command")
def get_command():
    global latest_command
    cmd = latest_command
    latest_command = "none"
    return {"command": cmd}

@app.post("/esp32/command/{cmd}")
def send_command(cmd: str):
    global latest_command
    if cmd in ["pump_on", "pump_off"]:
        latest_command = cmd
        return {"status": "command set"}
    return {"status": "invalid command"}

@app.get("/")
def read_root():
    return {"message": "FastAPI is working"}

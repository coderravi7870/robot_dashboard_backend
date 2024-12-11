from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import asyncio
from datetime import datetime

app = FastAPI()

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load initial data from 'fake_robot_data.json'
with open("fake_robot_data.json", "r") as f:
    robot_data = json.load(f)

# API to fetch robots
@app.get("/robots")
async def get_robots():
    return JSONResponse(content=robot_data)

# WebSocket for real-time updates
@app.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Simulate robot data updates every 5 seconds
        for robot in robot_data:
            # Update battery, CPU, RAM, Online status, and Last Updated time
            robot["Battery Percentage"] = max(0, robot["Battery Percentage"] - random.randint(0, 2))
            robot["CPU Usage"] = random.randint(10, 90)
            robot["RAM Consumption"] = random.randint(2000, 8000)
            robot["Online/Offline"] = random.choice([True, False])
            robot["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Randomly update location coordinates (Latitude and Longitude)
            robot["Location Coordinates"][0] += random.uniform(-0.01, 0.01)  # Latitude
            robot["Location Coordinates"][1] += random.uniform(-0.01, 0.01)  # Longitude

        # Send the updated robot data to WebSocket
        await websocket.send_json(robot_data)
        
        # Wait 5 seconds before the next update
        await asyncio.sleep(5)

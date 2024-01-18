from app import socketio
import random



places = [
    {"name": "Place A", "location": {"lat": 37.7749, "lng": -122.4194}},
    {"name": "Place B", "location": {"lat": 34.0522, "lng": -118.2437}},
    # ... add more places
]

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

def get_distance_and_duration(origin, destination, travel_mode):
    # Simulate distance and duration
    distance = round(random.uniform(1, 10), 2)
    duration = round(random.uniform(1, 30), 2)
    return {"distance": distance, "duration": duration}
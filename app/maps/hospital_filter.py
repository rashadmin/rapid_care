from flask import Flask, jsonify
from flask_socketio import emit
import time
from math import radians, sin, cos, sqrt, atan2
import pandas as pd
import random
import json
import numpy as np




def get_distance_and_duration(origin, destination):
    # Simulate distance and duration
    distance = round(random.uniform(1, 10), 2)
    duration = round(random.uniform(1, 30), 2)
    
    return {"distance": distance, "duration": duration}

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of Earth in kilometers
    return distance

def get_places_info():
    json_file_path = "app/maps/google_places.json"
    with open(json_file_path, 'r') as j:
        contents = json.loads(j.read())
    data = pd.DataFrame().from_dict(contents['places'])
    #data = data[~data['currentOpeningHours'].isna()].reset_index(drop=True)
    lat1, lon1 = 52.6749, -1.14194
    #if data['currentOpeningHours']:
    data['dist_km'] = data['location'].apply(lambda x: haversine(lat1, lon1,x['latitude'],x['longitude']))
    data = data[data['dist_km']<=5].reset_index(drop=True)
    data.drop('currentOpeningHours',axis=1,inplace=True)
    data['acceptance_probability'] = np.random.uniform(0,1,size=data.shape[0])
    data['duration'] = np.random.uniform(1,5,size=data.shape[0])
    data['ambulance'] = np.random.choice(np.array(['yes','no']),size=data.shape[0])
    data['displayName'] = data['displayName'].apply(lambda x: x['text'])
    data =data[data['acceptance_probability']<0.5]
    print(data)
    data = data.sort_values(['duration','dist_km'])[['displayName','dist_km','duration']].reset_index(drop=True)
    return jsonify(data.to_dict(orient='index'))#.apply(lambda x: x['dist_km']).to_dict()


def handle_get_places_data():
    while True:
        places_data = get_places_info()
        emit("update_places_data", places_data)
        time.sleep(1)

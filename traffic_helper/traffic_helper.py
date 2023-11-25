# traffic_helper.py
import requests
from config import MAPBOX_TOKEN, TOMTOM_API_KEY

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
TOM_TRAFFIC_DATA_BASE_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

def get_traffic_data(api_endpoint, params):
    response = requests.get(api_endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def process_raw_data(raw_data):
    processed_data = []
    # Adjust according to the actual structure of the TomTom API response
    for item in raw_data['flowSegmentData']:
        processed_data.append({
            'currentSpeed': item.get('currentSpeed', 'Not Available'),
            'freeFlowSpeed': item.get('freeFlowSpeed', 'Not Available'),
            'currentTravelTime': item.get('currentTravelTime', 'Not Available'),
            'freeFlowTravelTime': item.get('freeFlowTravelTime', 'Not Available'),
        })
    return processed_data

def calculate_traffic_flow(data):
    total_speed = sum(item['currentSpeed'] for item in data if 'currentSpeed' in item)
    average_speed = total_speed / len(data) if data else 0
    return average_speed

def analyze_traffic_for_route(route_coordinates):
    params = {
        'key': TOMTOM_API_KEY,
        'point': route_coordinates,
        # Add additional parameters as required by the API
    }
    raw_data = get_traffic_data(TOM_TRAFFIC_DATA_BASE_URL, params)
    processed_data = process_raw_data(raw_data)
    traffic_flow = calculate_traffic_flow(processed_data)
    return traffic_flow

def log_activity(message):
    
    print(message)

def main():
    # Example coordinates for a location on I-95
    route_coordinates = '25.782545,-80.299676'
    traffic_info = analyze_traffic_for_route(route_coordinates)
    print(traffic_info)

if __name__ == '__main__':
    main()

import requests
from config import MAPBOX_TOKEN, TRAFFIC_API_KEY

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
TOM_TRAFFIC_DATA_BASE_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

def geocode_location(location_name):
    geocoding_url = f"{MAPBOX_BASE_URL}/{location_name}.json"
    params = {'access_token': MAPBOX_TOKEN}
    response = requests.get(geocoding_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_traffic_data(api_endpoint, params):
    response = requests.get(api_endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def process_raw_data(raw_data):
    processed_data = []
    if 'flowSegmentData' in raw_data and isinstance(raw_data['flowSegmentData'], dict):
        item = raw_data['flowSegmentData']
        processed_data.append({
            'currentSpeed': item.get('currentSpeed', 'Not Available'),
            'freeFlowSpeed': item.get('freeFlowSpeed', 'Not Available'),
            'currentTravelTime': item.get('currentTravelTime', 'Not Available'),
            'freeFlowTravelTime': item.get('freeFlowTravelTime', 'Not Available'),
        })
    else:
        print("'flowSegmentData' is missing or not a dictionary.")
    return processed_data

def calculate_traffic_flow(data):
    total_speed = sum(item['currentSpeed'] for item in data if 'currentSpeed' in item)
    average_speed = total_speed / len(data) if data else 0
    return average_speed

def analyze_traffic_for_route(route_coordinates):
    params = {
        'key': TRAFFIC_API_KEY,
        'point': route_coordinates,
        # Add any other parameters required by the TomTom API
    }
    api_endpoint = TOM_TRAFFIC_DATA_BASE_URL
    raw_data = get_traffic_data(api_endpoint, params)
    processed_data = process_raw_data(raw_data)
    traffic_flow = calculate_traffic_flow(processed_data)
    return traffic_flow

def log_activity(message):
    print(message)


def main():
    location_name = 'New York, NY'
    geocoded_data = geocode_location(location_name)
    if geocoded_data and geocoded_data['features']:
        coordinates = geocoded_data['features'][0]['center']
        route_coordinates = f"{coordinates[1]},{coordinates[0]}"  # lat,lon
        traffic_info = analyze_traffic_for_route(route_coordinates)
        print(traffic_info)
    else:
        print("Geocoding failed.")

if __name__ == '__main__':
    main()

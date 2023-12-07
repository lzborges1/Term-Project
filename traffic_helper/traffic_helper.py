import requests
import sys
import logging
from datetime import datetime
import os

# Append the directory, not the file itself, to sys.path
sys.path.append(r"C:\Users\abattiata1\Apps\Desktop\Senior Year\Python\Term-Project")

from config import MAPBOX_TOKEN, TRAFFIC_API_KEY

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
TOM_TRAFFIC_DATA_BASE_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

# Set up basic configuration for logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_filename = datetime.now().strftime('traffic_helper_%Y_%m_%d.log')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{log_directory}/{log_filename}"),
        logging.StreamHandler()  # To also log to stdout
    ]
)

def log_exception(e):
    """
    Logs the exception with a timestamp.
    """
    logging.error("An exception occurred", exc_info=True)

def geocode_location(location_name):
    geocoding_url = f"{MAPBOX_BASE_URL}/{location_name}.json"
    params = {'access_token': MAPBOX_TOKEN}
    response = requests.get(geocoding_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        log_exception(Exception(f"Failed to geocode location: {location_name} with status code {response.status_code}"))
        response.raise_for_status()

def get_traffic_data(api_endpoint, params):
    response = requests.get(api_endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        log_exception(Exception(f"API endpoint call failed with status code {response.status_code}"))
        response.raise_for_status()

def process_raw_data(raw_data):
    processed_data = []
    if 'flowSegmentData' in raw_data and isinstance(raw_data['flowSegmentData'], dict):
        item = raw_data['flowSegmentData']
        processed_data.append({
            'currentSpeed': item.get('currentSpeed'),  # Ensure these keys match your frontend expectations
            'freeFlowSpeed': item.get('freeFlowSpeed'),
            'currentTravelTime': item.get('currentTravelTime'),
            'freeFlowTravelTime': item.get('freeFlowTravelTime'),
        })
    else:
        logging.error("'flowSegmentData' is missing or not a dictionary in the raw data.")
    return processed_data

def calculate_traffic_flow(data):
    total_speed = 0
    count = 0
    for item in data:
        try:
            # Attempt to get the currentSpeed and convert it to an integer.
            speed = int(item.get('currentSpeed', 0))
            if speed:  # Only add to total if speed is not zero.
                total_speed += speed
                count += 1
        except (TypeError, ValueError) as e:
            log_exception(e)
            # Log and ignore any items where currentSpeed is not an integer.
            log_activity(f"Non-numeric currentSpeed encountered: {item.get('currentSpeed')}")
    average_speed = total_speed / count if count > 0 else 0
    return average_speed

def analyze_traffic_for_route(route_coordinates):
    params = {
        'key': TRAFFIC_API_KEY,
        'point': route_coordinates,
    }
    api_endpoint = TOM_TRAFFIC_DATA_BASE_URL
    try:
        raw_data = get_traffic_data(api_endpoint, params)
        if not raw_data:
            raise ValueError("No data received from traffic API")
        
        log_activity(f"Raw data received: {raw_data}")

        processed_data = process_raw_data(raw_data)
        if not processed_data:
            raise ValueError("Failed to process raw traffic data")

        log_activity(f"Processed data: {processed_data}")

        traffic_flow = calculate_traffic_flow(processed_data)
        if traffic_flow is None:
            raise ValueError("Failed to calculate traffic flow")

        response = {
            'traffic_flow': traffic_flow,
            'details': processed_data,
        }
        log_activity(f"Response prepared: {response}")
        return response
    except ValueError as ve:
        log_exception(ve)
        return {'error': str(ve)}, 422
    except Exception as e:
        log_exception(e)
        return {'error': "An error occurred while analyzing traffic data"}, 500

def log_activity(message):
    logging.info(message)

def main():
    location_name = 'New York, NY'
    geocoded_data = geocode_location(location_name)
    if geocoded_data and geocoded_data['features']:
        coordinates = geocoded_data['features'][0]['center']
        route_coordinates = f"{coordinates[1]},{coordinates[0]}"  # lat,lon
        traffic_info = analyze_traffic_for_route(route_coordinates)
        log_activity(f"Traffic info: {traffic_info}")
    else:
        log_activity("Geocoding failed.")

if __name__ == '__main__':
    main()

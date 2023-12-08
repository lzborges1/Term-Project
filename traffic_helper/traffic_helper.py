import requests
import sys
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import traceback

# Set up basic configuration for logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_filename = datetime.now().strftime('traffic_helper_%Y_%m_%d.log')

# Initialize the logger
logger = logging.getLogger('TrafficAppLogger')
handler = logging.FileHandler(f"{log_directory}/{log_filename}")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Append the directory, not the file itself, to sys.path
sys.path.append(r"C:\Users\abattiata1\Apps\Desktop\Senior Year\Python\Term-Project")

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
        logger.error(f"Failed to geocode location: {location_name} with status code {response.status_code}", exc_info=True)
        response.raise_for_status()

def get_traffic_data(api_endpoint, params):
    response = requests.get(api_endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"API endpoint call failed with status code {response.status_code}", exc_info=True)
        response.raise_for_status()

def process_raw_data(raw_data):
    processed_data = []
    if 'flowSegmentData' in raw_data and isinstance(raw_data['flowSegmentData'], dict):
        item = raw_data['flowSegmentData']
        processed_data.append({
            'currentSpeed': item.get('currentSpeed'),
            'freeFlowSpeed': item.get('freeFlowSpeed'),
            'currentTravelTime': item.get('currentTravelTime'),
            'freeFlowTravelTime': item.get('freeFlowTravelTime'),
        })
    else:
        logger.error("'flowSegmentData' is missing or not a dictionary in the raw data.")
    return processed_data

def calculate_traffic_flow(data):
    total_speed = 0
    count = 0
    for item in data:
        try:
            speed = int(item.get('currentSpeed', 0))
            if speed:
                total_speed += speed
                count += 1
        except (TypeError, ValueError) as e:
            logger.error(f"Non-numeric currentSpeed encountered: {item.get('currentSpeed')}", exc_info=True)
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
            logger.error("No data received from traffic API")
            raise ValueError("No data received from traffic API")

        logger.info(f"Raw data received: {raw_data}")

        processed_data = process_raw_data(raw_data)
        if not processed_data:
            logger.error("Failed to process raw traffic data")
            raise ValueError("Failed to process raw traffic data")

        logger.info(f"Processed data: {processed_data}")

        traffic_flow = calculate_traffic_flow(processed_data)
        if traffic_flow is None:
            logger.error("Failed to calculate traffic flow")
            raise ValueError("Failed to calculate traffic flow")

        response = {
            'traffic_flow': traffic_flow,
            'details': processed_data,
        }
        logger.info(f"Response prepared: {response}")
        return response
    except ValueError as ve:
        logger.error(f"ValueError: {ve}", exc_info=True)
        return {'error': str(ve)}, 422
    except Exception as e:
        logger.error(f"Exception: {e}", exc_info=True)
        return {'error': "An error occurred while analyzing traffic data"}, 500

def main():
    logger.info("Starting geocoding process.")
    try:
        location_name = 'New York, NY'
        geocoded_data = geocode_location(location_name)
        if geocoded_data and geocoded_data['features']:
            coordinates = geocoded_data['features'][0]['center']
            route_coordinates = f"{coordinates[1]},{coordinates[0]}"  # lat,lon
            logger.info(f"Coordinates for {location_name}: {coordinates}")
            
            traffic_info = analyze_traffic_for_route(route_coordinates)
            if traffic_info:
                logger.info(f"Traffic info for {route_coordinates}: {traffic_info}")
            else:
                logger.warning(f"No traffic info available for {route_coordinates}")
        else:
            logger.error("Geocoding failed. No features found in the geocoded data.")
    except Exception as e:
        logger.error("An unexpected error occurred in the main function", exc_info=True)

if __name__ == '__main__':
    main()


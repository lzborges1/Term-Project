from flask import Flask, render_template, request, url_for, redirect, jsonify
from traffic_helper.traffic_helper import get_traffic_data, process_raw_data, calculate_traffic_flow, analyze_traffic_for_route
import os
import requests
from config import MAPBOX_TOKEN
from flask_cors import CORS
import traceback
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('traffic_app.log', maxBytes=10000, backupCount=3)
logger.addHandler(handler)

print(os.getcwd())

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

# Function to perform geocoding using Mapbox
def geocode_location(location_name):
    geocoding_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location_name}.json"
    params = {
        'access_token': MAPBOX_TOKEN
    }
    response = requests.get(geocoding_url, params=params)
    if response.status_code == 200:
        return response.json()['features'][0]['center']  # returns [longitude, latitude]
    else:
        response.raise_for_status()

@app.route('/get_traffic', methods=['POST'])
def get_traffic():
    try:
        # Ensure the request is in JSON format
        if not request.is_json:
            logger.error("Received non-JSON request")
            return jsonify({'error': 'Request body must be JSON'}), 400

        data = request.get_json()
        logger.info(f"Received JSON data: {data}")

        # Validate that 'start' and 'end' are in the data
        if 'start' not in data or 'end' not in data:
            logger.error("JSON data is missing 'start' or 'end' keys")
            return jsonify({'error': 'JSON body must contain start and end coordinates'}), 400

        start_coords = data['start']
        end_coords = data['end']

        # Validate the format of 'start' and 'end' coordinates
        if not (isinstance(start_coords, list) and len(start_coords) == 2):
            logger.error("Start coordinates are in the wrong format")
            return jsonify({'error': 'Start coordinates are not in the correct format'}), 400
        if not (isinstance(end_coords, list) and len(end_coords) == 2):
            logger.error("End coordinates are in the wrong format")
            return jsonify({'error': 'End coordinates are not in the correct format'}), 400

        # Format the coordinates for the traffic analysis function
        route_str = f"{start_coords[1]},{start_coords[0]}:{end_coords[1]},{end_coords[0]}"
        logger.info(f"Formatted route string for analysis: {route_str}")

        # Perform the traffic analysis
        traffic_info = analyze_traffic_for_route(route_str)

        # Check if there is an error in the traffic information
        if 'error' in traffic_info:
            error_message = traffic_info['error']
            logger.error(f"Traffic information error: {error_message}")
            return jsonify({'error': error_message}), 500
        
        # If no error, return the traffic information
        logger.info(f"Traffic information response: {traffic_info}")
        return jsonify(traffic_info)
    
    except KeyError as e:
        logger.error(f"KeyError: Missing key in JSON data: {e}", exc_info=True)
        return jsonify({'error': f'Missing data: {e}'}), 400
    except Exception as e:
        logger.error(f"Exception: Error getting traffic data: {e}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/traffic', methods=['GET'])
def traffic():
    location_name = 'New York, NY'
    coordinates = geocode_location(location_name)
    route_coordinates = f"{coordinates[1]},{coordinates[0]}"
    return render_template('result.html', data={'coordinates': route_coordinates})

@app.route('/submit', methods=['POST'])
def submit():
    return redirect(url_for('traffic'))

if __name__ == '__main__':
    app.run(debug=True)

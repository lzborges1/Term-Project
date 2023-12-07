from flask import Flask, render_template, request, url_for, redirect, jsonify
from traffic_helper.traffic_helper import get_traffic_data, process_raw_data, calculate_traffic_flow, analyze_traffic_for_route
import os
import requests
from config import MAPBOX_TOKEN
from flask_cors import CORS
import traceback

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
        if not request.is_json:
            print("Received non-JSON request")
            return jsonify({'error': 'Request body must be JSON'}), 400

        data = request.get_json()
        print(f"Received JSON data: {data}")  # Log the raw JSON data

        if 'start' not in data or 'end' not in data:
            print("JSON data is missing 'start' or 'end' keys")
            return jsonify({'error': 'JSON body must contain start and end coordinates'}), 400

        start_coords = data['start']
        end_coords = data['end']

        if not isinstance(start_coords, (list, tuple)) or len(start_coords) != 2:
            print(f"Start coordinates are in the wrong format: {start_coords}")
            return jsonify({'error': 'Start coordinates are not in the correct format'}), 400
        if not isinstance(end_coords, (list, tuple)) or len(end_coords) != 2:
            print(f"End coordinates are in the wrong format: {end_coords}")
            return jsonify({'error': 'End coordinates are not in the correct format'}), 400

        route_str = f"{start_coords[1]},{start_coords[0]}:{end_coords[1]},{end_coords[0]}"
        print(f"Formatted route string for analysis: {route_str}")  # Log the route string

        traffic_info = analyze_traffic_for_route(route_str)

        if not traffic_info or 'error' in traffic_info:
            error_message = traffic_info.get('error', 'No traffic information found')
            print(f"Traffic information error: {error_message}")
            return jsonify({'error': error_message}), 500

        print(f"Traffic information response: {traffic_info}")  # Log the successful traffic info response
        return jsonify(traffic_info)

    except KeyError as e:
        print(f"KeyError: Missing key in JSON data: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Missing data: ' + str(e)}), 400
    except Exception as e:
        print(f"Exception: Error getting traffic data: {e}")
        traceback.print_exc()
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

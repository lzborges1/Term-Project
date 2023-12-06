from flask import Flask, render_template, request, url_for, redirect, jsonify
from traffic_helper.traffic_helper import get_traffic_data, process_raw_data, calculate_traffic_flow, analyze_traffic_for_route
import os
import requests
from config import MAPBOX_TOKEN
from flask_cors import CORS

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

# New route to handle traffic data requests
@app.route('/get_traffic', methods=['POST'])
def get_traffic():
    try:
        data = request.json
        start_coords = data['start']
        end_coords = data['end']
        
        # Ensure the coordinates are provided
        if not start_coords or not end_coords:
            return jsonify({'error': 'Missing start or end coordinates'}), 400
        
        start_str = f"{start_coords[1]},{start_coords[0]}"  # Ensure correct ordering for lat,lon
        end_str = f"{end_coords[1]},{end_coords[0]}"

        traffic_info = analyze_traffic_for_route(start_str, end_str)  # Function from your traffic_helper.py
        
        # Check if the traffic_info is not empty or null
        if not traffic_info:
            return jsonify({'error': 'No traffic information found'}), 404
        
        return jsonify(traffic_info)
    except Exception as e:
        # Log the exception to the console or a file
        print(f"Error getting traffic data: {e}")
        
        # Return a JSON response with the error message and a 500 status code
        return jsonify({'error': str(e)}), 500

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

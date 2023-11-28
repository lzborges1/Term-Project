from flask import Flask, render_template, request, url_for, redirect
from traffic_helper import get_traffic_data, process_raw_data, calculate_traffic_flow, analyze_traffic_for_route
import os

print(os.getcwd())

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

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

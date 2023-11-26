from flask import Flask, render_template, request, url_for, redirect
import requests
import urllib.parse
from traffic_helper import get_traffic_data, process_raw_data, calculate_traffic_flow, analyze_traffic_for_route
from config import MAPBOX_TOKEN, TRAFFIC_API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traffic', methods=['GET'])
def traffic():
    # Assuming you have predefined coordinates for I-95 or you get them from the user somehow
    route_coordinates = 'specific_latitude,specific_longitude'
    traffic_data = analyze_traffic_for_route(route_coordinates)
    return render_template('result.html', data=traffic_data)

@app.route('/submit', methods=['POST'])
def submit():
    return redirect(url_for('traffic'))

if __name__ == '__main__':
    app.run(debug=True)


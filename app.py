from flask import Flask, request, jsonify, render_template
import requests
import mysql.connector
import numpy as np

app = Flask(__name__)

# Google API key 
Google_Key = "AIzaSyAQpwvYBCrZVd12jxGEFKWDEz1B2WyeDzA"
user = "root"
passwrd = "root"
host = "localhost"
database = "drive_smart_texas"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_route_data', methods=['POST'])

def get_route_data():
    # Get addresses and time of day
    start_address = request.form.get('start_address')
    end_address = request.form.get('end_address')
    time_of_day = request.form.get('time_of_day')
    weather = request.form.get('weather')
    # Weather

    # Convert start and end addresses to lat, long using Google API
    start_lat, start_lng = get_lat_lng(start_address)
    end_lat, end_lng = get_lat_lng(end_address)

    # Query MySQL database
    route_data = query_database(start_lat, start_lng, end_lat, end_lng, time_of_day)

    # Results
    return route_data['message']



@app.route('/report_accident', methods=['POST'])
def report_accident():
    # Get the report data
    location = request.form.get('location')
    severity = int(request.form.get('severity'))
    description = request.form.get('description')
    sunrise_sunset = request.form.get('sunrise_sunset')

    # Convert the location to lat, long
    lat, lng = get_lat_lng(location)

    # Insert a new row in database
    insert_to_database(lat, lng, severity, description, sunrise_sunset)

    return "Thank you for reporting the accident."

def get_lat_lng(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={Google_Key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        lat_lng = data['results'][0]['geometry']['location']
        return lat_lng['lat'], lat_lng['lng']
    else:
        return None, None

def query_database(start_lat, start_lng, end_lat, end_lng, time_of_day):
    conn = mysql.connector.connect(user=user, password= passwrd, host= host, database=database, port=8889)
    c = conn.cursor()
    
    # Query based on user route data- add weather condition as WHERE condition, join on weather attributes
    query = """
        SELECT Severity FROM traffic_attributes
        WHERE Start_Lat BETWEEN %s AND %s
        AND Start_Lng BETWEEN %s AND %s
        AND Sunrise_Sunset = %s
    """
    parameters = (min(start_lat, end_lat), max(start_lat, end_lat), min(start_lng, end_lng), max(start_lng, end_lng), time_of_day)

    c.execute(query, parameters)
    results = c.fetchall()

    conn.close()

    # Average severity
    avg_severity = np.mean([row[0] for row in results])
    num_accidents = len(results)

    # Construct a message based on the average severity
    if avg_severity < 3:
        message = f"{num_accidents} accidents have been reported on this route with an average severity level: mild"
    elif avg_severity >= 3 and avg_severity <= 3.5:
        message = f"{num_accidents} accidents have been reported on this route with an average severity level: moderate"
    else:
        message = f"{num_accidents} accidents have been reported on this route with an average severity level: severe"

    return {'message': message}

def insert_to_database(lat, lng, severity, description, sunrise_sunset):
    conn = mysql.connector.connect(user=user, password=passwrd, host=host, database=database, port=8889)
    c = conn.cursor()

    # Highest current Incident_ID
    c.execute("SELECT Incident_ID FROM traffic_attributes ORDER BY Incident_ID DESC LIMIT 1")
    result = c.fetchone()

    # Increment the numeric part of the ID by 1
    if result:
        last_id = result[0]
        num_part = int(last_id.split('-')[1]) + 1
    else:
        num_part = 1

    new_id = f"A-{num_part}"

    # Insert the data
    query = """
        INSERT INTO traffic_attributes (Incident_ID, Start_Lat, Start_Lng, Severity, Description, Sunrise_Sunset)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    parameters = (new_id, lat, lng, severity, description, sunrise_sunset)

    c.execute(query, parameters)


if __name__ == '__main__':
    app.run(debug=True, port = 5002)